"""
PDF Processing Tools
Allows agent to read and extract information from PDF files
"""
import os
from typing import Optional, List, Dict, Any
from tools import Tool, ToolResult
import PyPDF2
import io


class PDFReaderTool(Tool):
    """Tool for reading and extracting text from PDF files"""
    
    def __init__(self):
        super().__init__(
            name="read_pdf",
            description="Read and extract text from PDF files. Parameters: path (PDF file path), pages (optional, specific pages to read)"
        )
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - Path to PDF file (e.g., 'documents/report.pdf')",
                "pages": "string (optional) - Page range (e.g., '1-5', '1,3,5', 'all')"
            }
        }
    
    def execute(self, path: str, pages: str = "all") -> ToolResult:
        """Extract text from PDF"""
        try:
            # Check if file exists
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"PDF file not found: {path}"
                )
            
            # Check if it's a PDF
            if not path.lower().endswith('.pdf'):
                return ToolResult(
                    success=False,
                    output="",
                    error="File must be a PDF (.pdf extension)"
                )
            
            # Open and read PDF
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                # Parse page range
                page_numbers = self._parse_page_range(pages, total_pages)
                
                # Extract text
                extracted_text = []
                for page_num in page_numbers:
                    if 0 <= page_num < total_pages:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        extracted_text.append(f"--- Page {page_num + 1} ---\n{text}\n")
                
                if not extracted_text:
                    return ToolResult(
                        success=False,
                        output="",
                        error="No text could be extracted from the specified pages"
                    )
                
                # Format output
                output = f"PDF: {os.path.basename(path)}\n"
                output += f"Total Pages: {total_pages}\n"
                output += f"Extracted Pages: {len(extracted_text)}\n\n"
                output += "\n".join(extracted_text)
                
                # Limit output size
                if len(output) > 10000:
                    output = output[:10000] + f"\n\n[Truncated. Total length: {len(output)} characters]"
                
                return ToolResult(success=True, output=output)
        
        except PyPDF2.errors.PdfReadError as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error reading PDF: {str(e)}. File may be corrupted or encrypted."
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error processing PDF: {str(e)}"
            )
    
    def _parse_page_range(self, pages: str, total_pages: int) -> List[int]:
        """Parse page range string into list of page numbers (0-indexed)"""
        if pages.lower() == "all":
            return list(range(total_pages))
        
        page_numbers = []
        parts = pages.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                # Range like "1-5"
                start, end = part.split('-')
                start = int(start.strip()) - 1  # Convert to 0-indexed
                end = int(end.strip())
                page_numbers.extend(range(start, end))
            else:
                # Single page like "3"
                page_numbers.append(int(part) - 1)  # Convert to 0-indexed
        
        return sorted(set(page_numbers))  # Remove duplicates and sort


class PDFInfoTool(Tool):
    """Tool for getting PDF metadata and information"""
    
    def __init__(self):
        super().__init__(
            name="pdf_info",
            description="Get metadata and information about a PDF file. Parameters: path (PDF file path)"
        )
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - Path to PDF file"
            }
        }
    
    def execute(self, path: str) -> ToolResult:
        """Get PDF metadata"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"PDF file not found: {path}"
                )
            
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Get metadata
                metadata = pdf_reader.metadata
                num_pages = len(pdf_reader.pages)
                
                # Format output
                output = f"PDF Information: {os.path.basename(path)}\n\n"
                output += f"Number of Pages: {num_pages}\n"
                output += f"File Size: {os.path.getsize(path) / 1024:.2f} KB\n\n"
                
                if metadata:
                    output += "Metadata:\n"
                    if metadata.title:
                        output += f"  Title: {metadata.title}\n"
                    if metadata.author:
                        output += f"  Author: {metadata.author}\n"
                    if metadata.subject:
                        output += f"  Subject: {metadata.subject}\n"
                    if metadata.creator:
                        output += f"  Creator: {metadata.creator}\n"
                    if metadata.producer:
                        output += f"  Producer: {metadata.producer}\n"
                    if metadata.creation_date:
                        output += f"  Created: {metadata.creation_date}\n"
                    if metadata.modification_date:
                        output += f"  Modified: {metadata.modification_date}\n"
                else:
                    output += "No metadata available\n"
                
                # Check if encrypted
                if pdf_reader.is_encrypted:
                    output += "\n⚠️ PDF is encrypted/password protected\n"
                
                return ToolResult(success=True, output=output)
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error getting PDF info: {str(e)}"
            )


class PDFSearchTool(Tool):
    """Tool for searching text within PDF files"""
    
    def __init__(self):
        super().__init__(
            name="search_pdf",
            description="Search for text within a PDF file. Parameters: path (PDF file path), query (text to search for)"
        )
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - Path to PDF file",
                "query": "string - Text to search for"
            }
        }
    
    def execute(self, path: str, query: str) -> ToolResult:
        """Search for text in PDF"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"PDF file not found: {path}"
                )
            
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                # Search through pages
                results = []
                query_lower = query.lower()
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    if query_lower in text.lower():
                        # Find context around the match
                        lines = text.split('\n')
                        matching_lines = [
                            (i, line) for i, line in enumerate(lines)
                            if query_lower in line.lower()
                        ]
                        
                        for line_num, line in matching_lines:
                            # Get context (line before and after)
                            context_start = max(0, line_num - 1)
                            context_end = min(len(lines), line_num + 2)
                            context = '\n'.join(lines[context_start:context_end])
                            
                            results.append({
                                'page': page_num + 1,
                                'context': context.strip()
                            })
                
                if not results:
                    return ToolResult(
                        success=True,
                        output=f"No matches found for '{query}' in {os.path.basename(path)}"
                    )
                
                # Format output
                output = f"Found {len(results)} matches for '{query}' in {os.path.basename(path)}:\n\n"
                
                for i, result in enumerate(results[:10], 1):  # Limit to 10 results
                    output += f"{i}. Page {result['page']}:\n"
                    output += f"   {result['context']}\n\n"
                
                if len(results) > 10:
                    output += f"... and {len(results) - 10} more matches\n"
                
                return ToolResult(success=True, output=output)
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error searching PDF: {str(e)}"
            )


class ScanDirectoryForPDFsTool(Tool):
    """Tool for finding PDF files in a directory"""
    
    def __init__(self):
        super().__init__(
            name="find_pdfs",
            description="Find all PDF files in a directory. Parameters: path (directory path), recursive (optional, search subdirectories)"
        )
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - Directory path to search (default: current directory)",
                "recursive": "boolean (optional) - Search subdirectories (default: false)"
            }
        }
    
    def execute(self, path: str = ".", recursive: bool = False) -> ToolResult:
        """Find PDF files in directory"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Directory not found: {path}"
                )
            
            if not os.path.isdir(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Not a directory: {path}"
                )
            
            pdf_files = []
            
            if recursive:
                # Recursive search
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            full_path = os.path.join(root, file)
                            size = os.path.getsize(full_path)
                            pdf_files.append({
                                'path': full_path,
                                'name': file,
                                'size': size
                            })
            else:
                # Non-recursive search
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path) and item.lower().endswith('.pdf'):
                        size = os.path.getsize(full_path)
                        pdf_files.append({
                            'path': full_path,
                            'name': item,
                            'size': size
                        })
            
            if not pdf_files:
                return ToolResult(
                    success=True,
                    output=f"No PDF files found in {path}"
                )
            
            # Sort by name
            pdf_files.sort(key=lambda x: x['name'])
            
            # Format output
            output = f"Found {len(pdf_files)} PDF file(s) in {path}:\n\n"
            
            for pdf in pdf_files:
                size_kb = pdf['size'] / 1024
                output += f"📄 {pdf['name']}\n"
                output += f"   Path: {pdf['path']}\n"
                output += f"   Size: {size_kb:.2f} KB\n\n"
            
            return ToolResult(success=True, output=output)
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error scanning directory: {str(e)}"
            )
