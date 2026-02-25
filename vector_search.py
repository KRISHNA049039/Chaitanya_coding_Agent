"""
Vector Search with Semantic Embeddings
Enables semantic search over conversations, documents, and code
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import json
import os
import pickle
from datetime import datetime


class VectorStore:
    """In-memory vector store with semantic search"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize vector store
        
        Args:
            model_name: Sentence transformer model to use
                       'all-MiniLM-L6-v2' - Fast, 384 dimensions (default)
                       'all-mpnet-base-v2' - Better quality, 768 dimensions
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Storage
        self.embeddings = []  # List of numpy arrays
        self.documents = []   # List of document dicts
        self.index = 0
        
        print(f"✓ Vector store initialized (dimension: {self.dimension})")
    
    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Add a document to the vector store
        
        Args:
            content: Text content to embed
            metadata: Additional metadata (session_id, timestamp, etc.)
        
        Returns:
            Document ID
        """
        # Generate embedding
        embedding = self.model.encode(content, convert_to_numpy=True)
        
        # Store
        doc_id = self.index
        self.embeddings.append(embedding)
        self.documents.append({
            'id': doc_id,
            'content': content,
            'metadata': metadata or {},
            'created_at': datetime.utcnow().isoformat()
        })
        self.index += 1
        
        return doc_id
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[int]:
        """
        Add multiple documents at once (faster)
        
        Args:
            documents: List of dicts with 'content' and optional 'metadata'
        
        Returns:
            List of document IDs
        """
        contents = [doc['content'] for doc in documents]
        
        # Batch encode for efficiency
        embeddings = self.model.encode(contents, convert_to_numpy=True, show_progress_bar=True)
        
        doc_ids = []
        for i, (content, embedding) in enumerate(zip(contents, embeddings)):
            doc_id = self.index
            self.embeddings.append(embedding)
            self.documents.append({
                'id': doc_id,
                'content': content,
                'metadata': documents[i].get('metadata', {}),
                'created_at': datetime.utcnow().isoformat()
            })
            self.index += 1
            doc_ids.append(doc_id)
        
        return doc_ids
    
    def search(self, query: str, top_k: int = 5, filter_metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Semantic search for similar documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Filter by metadata (e.g., {'session_id': 'abc123'})
        
        Returns:
            List of documents with similarity scores
        """
        if not self.embeddings:
            return []
        
        # Encode query
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        
        # Calculate cosine similarity
        embeddings_array = np.array(self.embeddings)
        similarities = np.dot(embeddings_array, query_embedding) / (
            np.linalg.norm(embeddings_array, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Filter by metadata if specified
        valid_indices = range(len(self.documents))
        if filter_metadata:
            valid_indices = [
                i for i in valid_indices
                if all(
                    self.documents[i]['metadata'].get(k) == v
                    for k, v in filter_metadata.items()
                )
            ]
        
        # Get top-k results from valid indices
        valid_similarities = [(i, similarities[i]) for i in valid_indices]
        top_indices = sorted(valid_similarities, key=lambda x: x[1], reverse=True)[:top_k]
        
        # Format results
        results = []
        for idx, score in top_indices:
            doc = self.documents[idx].copy()
            doc['similarity'] = float(score)
            results.append(doc)
        
        return results
    
    def get_document(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        if 0 <= doc_id < len(self.documents):
            return self.documents[doc_id]
        return None
    
    def delete_document(self, doc_id: int) -> bool:
        """Delete document by ID"""
        if 0 <= doc_id < len(self.documents):
            # Mark as deleted (don't actually remove to keep indices stable)
            self.documents[doc_id]['deleted'] = True
            return True
        return False
    
    def save(self, filepath: str):
        """Save vector store to disk"""
        data = {
            'embeddings': self.embeddings,
            'documents': self.documents,
            'index': self.index,
            'dimension': self.dimension
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"✓ Vector store saved to {filepath}")
    
    def load(self, filepath: str):
        """Load vector store from disk"""
        if not os.path.exists(filepath):
            print(f"No saved vector store found at {filepath}")
            return False
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.embeddings = data['embeddings']
        self.documents = data['documents']
        self.index = data['index']
        print(f"✓ Vector store loaded from {filepath} ({len(self.documents)} documents)")
        return True
    
    def stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        active_docs = [d for d in self.documents if not d.get('deleted', False)]
        return {
            'total_documents': len(self.documents),
            'active_documents': len(active_docs),
            'dimension': self.dimension,
            'model': self.model.get_sentence_embedding_dimension()
        }


class ConversationSearcher:
    """Semantic search over conversation history"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def index_conversation(self, session_id: str, messages: List[Dict[str, str]]):
        """
        Index a conversation for semantic search
        
        Args:
            session_id: Session identifier
            messages: List of message dicts with 'role' and 'content'
        """
        documents = []
        for msg in messages:
            if msg['content'].strip():  # Skip empty messages
                documents.append({
                    'content': msg['content'],
                    'metadata': {
                        'session_id': session_id,
                        'role': msg['role'],
                        'type': 'conversation'
                    }
                })
        
        if documents:
            self.vector_store.add_documents(documents)
            print(f"✓ Indexed {len(documents)} messages from session {session_id}")
    
    def search_conversations(self, query: str, top_k: int = 5, session_id: Optional[str] = None) -> List[Dict]:
        """
        Search across all conversations
        
        Args:
            query: Search query
            top_k: Number of results
            session_id: Optional filter by session
        
        Returns:
            List of relevant messages with context
        """
        filter_meta = {'type': 'conversation'}
        if session_id:
            filter_meta['session_id'] = session_id
        
        return self.vector_store.search(query, top_k=top_k, filter_metadata=filter_meta)
    
    def find_similar_questions(self, question: str, top_k: int = 3) -> List[Dict]:
        """Find similar questions asked before"""
        results = self.search_conversations(question, top_k=top_k)
        return [r for r in results if r['metadata']['role'] == 'user']


class CodeSearcher:
    """Semantic search over code snippets"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def index_code_file(self, filepath: str, content: str, language: str = 'python'):
        """
        Index a code file
        
        Args:
            filepath: Path to the file
            content: File content
            language: Programming language
        """
        # Split into chunks (functions, classes, etc.)
        chunks = self._split_code(content, language)
        
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                'content': chunk,
                'metadata': {
                    'filepath': filepath,
                    'language': language,
                    'chunk_index': i,
                    'type': 'code'
                }
            })
        
        if documents:
            self.vector_store.add_documents(documents)
            print(f"✓ Indexed {len(documents)} code chunks from {filepath}")
    
    def _split_code(self, content: str, language: str) -> List[str]:
        """Split code into meaningful chunks"""
        # Simple splitting by functions/classes
        # In production, use tree-sitter or similar for proper parsing
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            current_chunk.append(line)
            
            # Split on function/class definitions (simple heuristic)
            if language == 'python':
                if line.strip().startswith(('def ', 'class ')) and len(current_chunk) > 1:
                    chunks.append('\n'.join(current_chunk[:-1]))
                    current_chunk = [line]
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return [c for c in chunks if c.strip()]
    
    def search_code(self, query: str, top_k: int = 5, language: Optional[str] = None) -> List[Dict]:
        """
        Search for relevant code snippets
        
        Args:
            query: Natural language query or code snippet
            top_k: Number of results
            language: Optional filter by language
        
        Returns:
            List of relevant code chunks
        """
        filter_meta = {'type': 'code'}
        if language:
            filter_meta['language'] = language
        
        return self.vector_store.search(query, top_k=top_k, filter_metadata=filter_meta)


# Global instances
vector_store = VectorStore()
conversation_searcher = ConversationSearcher(vector_store)
code_searcher = CodeSearcher(vector_store)


# Auto-load saved vector store
VECTOR_STORE_PATH = 'vector_store.pkl'
if os.path.exists(VECTOR_STORE_PATH):
    vector_store.load(VECTOR_STORE_PATH)


def save_vector_store():
    """Save vector store to disk"""
    vector_store.save(VECTOR_STORE_PATH)


if __name__ == "__main__":
    # Test the vector store
    print("Testing Vector Search...")
    
    # Add some test documents
    docs = [
        {"content": "Python is a high-level programming language", "metadata": {"type": "test"}},
        {"content": "Machine learning uses neural networks", "metadata": {"type": "test"}},
        {"content": "JavaScript is used for web development", "metadata": {"type": "test"}},
    ]
    
    vector_store.add_documents(docs)
    
    # Search
    results = vector_store.search("programming languages", top_k=2)
    
    print("\nSearch results:")
    for r in results:
        print(f"- {r['content']} (similarity: {r['similarity']:.3f})")
    
    print("\n✓ Vector search working!")
