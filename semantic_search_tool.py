"""
Semantic Search Tool for Agent
Allows agent to search conversations and code semantically
"""
from tools import Tool, ToolResult
from vector_search import conversation_searcher, code_searcher, vector_store
from typing import Optional
import json


class SemanticSearchTool(Tool):
    """Tool for semantic search over conversations"""
    
    def __init__(self):
        super().__init__(
            name="semantic_search",
            description="Search previous conversations semantically. Parameters: query (what to search for), top_k (number of results, default 5)"
        )
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "query": "string - What to search for (e.g., 'how to use async in Python')",
                "top_k": "integer (optional) - Number of results (default: 5)"
            }
        }
    
    def execute(self, query: str, top_k: int = 5) -> ToolResult:
        """Search conversations semantically"""
        try:
            results = conversation_searcher.search_conversations(query, top_k=top_k)
            
            if not results:
                return ToolResult(
                    success=True,
                    output="No relevant conversations found."
                )
            
            # Format results
            output = f"Found {len(results)} relevant conversations:\n\n"
            for i, result in enumerate(results, 1):
                similarity = result['similarity']
                content = result['content'][:200]  # Truncate long content
                role = result['metadata'].get('role', 'unknown')
                
                output += f"{i}. [{role}] (similarity: {similarity:.2f})\n"
                output += f"   {content}...\n\n"
            
            return ToolResult(success=True, output=output)
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Search failed: {str(e)}"
            )


class CodeSearchTool(Tool):
    """Tool for semantic search over code"""
    
    def __init__(self):
        super().__init__(
            name="search_code",
            description="Search code snippets semantically. Parameters: query (what to search for), language (optional filter)"
        )
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "query": "string - What to search for (e.g., 'function to validate email')",
                "language": "string (optional) - Filter by language (e.g., 'python', 'javascript')"
            }
        }
    
    def execute(self, query: str, language: Optional[str] = None) -> ToolResult:
        """Search code semantically"""
        try:
            results = code_searcher.search_code(query, top_k=5, language=language)
            
            if not results:
                return ToolResult(
                    success=True,
                    output="No relevant code found."
                )
            
            # Format results
            output = f"Found {len(results)} relevant code snippets:\n\n"
            for i, result in enumerate(results, 1):
                similarity = result['similarity']
                content = result['content']
                filepath = result['metadata'].get('filepath', 'unknown')
                lang = result['metadata'].get('language', 'unknown')
                
                output += f"{i}. {filepath} ({lang}) - similarity: {similarity:.2f}\n"
                output += f"```{lang}\n{content}\n```\n\n"
            
            return ToolResult(success=True, output=output)
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Code search failed: {str(e)}"
            )
