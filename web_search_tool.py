"""
Web Search and URL Fetching Tools
Allows agent to search the internet and fetch content from URLs
"""
import requests
from bs4 import BeautifulSoup
import json
from typing import Optional, Dict, Any
from tools import Tool, ToolResult
import re


class WebSearchTool(Tool):
    """Tool for searching the internet using DuckDuckGo"""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the internet for information. Parameters: query (search query), num_results (optional, default 5)"
        )
    
    def schema(self):
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "query": "string - Search query (e.g., 'Python tutorials', 'latest AI news')",
                "num_results": "integer (optional) - Number of results to return (default: 5, max: 10)"
            }
        }
    
    def execute(self, query: str, num_results: int = 5) -> ToolResult:
        """Search using DuckDuckGo (no API key needed)"""
        try:
            # Limit results
            num_results = min(num_results, 10)
            
            # DuckDuckGo HTML search
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result')[:num_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
            
            if not results:
                return ToolResult(
                    success=False,
                    output="",
                    error="No results found. Try a different query."
                )
            
            # Format results nicely
            output = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                output += f"{i}. {result['title']}\n"
                output += f"   URL: {result['url']}\n"
                if result['snippet']:
                    output += f"   {result['snippet']}\n"
                output += "\n"
            
            return ToolResult(
                success=True,
                output=output.strip()
            )
        
        except requests.exceptions.Timeout:
            return ToolResult(
                success=False,
                output="",
                error="Search request timed out"
            )
        except requests.exceptions.RequestException as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Search failed: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error during search: {str(e)}"
            )


class FetchURLTool(Tool):
    """Tool for fetching and extracting content from URLs"""
    
    def __init__(self):
        super().__init__(
            name="fetch_url",
            description="Fetch and extract text content from a URL. Parameters: url (webpage URL), max_length (optional, default 5000)"
        )
    
    def schema(self):
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "url": "string - URL to fetch (e.g., 'https://example.com/article')",
                "max_length": "integer (optional) - Maximum characters to return (default: 5000)"
            }
        }
    
    def execute(self, url: str, max_length: int = 5000) -> ToolResult:
        """Fetch and extract text from URL"""
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                return ToolResult(
                    success=False,
                    output="",
                    error="Invalid URL. Must start with http:// or https://"
                )
            
            # Fetch URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit length
            if len(text) > max_length:
                text = text[:max_length] + f"\n\n[Content truncated. Total length: {len(text)} characters]"
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "No title"
            
            output = f"Title: {title_text}\n"
            output += f"URL: {url}\n"
            output += f"Content length: {len(text)} characters\n\n"
            output += text
            
            return ToolResult(
                success=True,
                output=output
            )
        
        except requests.exceptions.Timeout:
            return ToolResult(
                success=False,
                output="",
                error="Request timed out. URL took too long to respond."
            )
        except requests.exceptions.HTTPError as e:
            return ToolResult(
                success=False,
                output="",
                error=f"HTTP error: {e.response.status_code} - {e.response.reason}"
            )
        except requests.exceptions.RequestException as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Failed to fetch URL: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error processing URL: {str(e)}"
            )


class QuickAnswerTool(Tool):
    """Tool for getting quick answers using DuckDuckGo Instant Answers"""
    
    def __init__(self):
        super().__init__(
            name="quick_answer",
            description="Get quick factual answers. Parameters: query (question or topic)"
        )
    
    def schema(self):
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "query": "string - Question or topic (e.g., 'What is Python?', 'Einstein birthday')"
            }
        }
    
    def execute(self, query: str) -> ToolResult:
        """Get instant answer from DuckDuckGo"""
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract answer
            answer = data.get('AbstractText') or data.get('Answer') or data.get('Definition')
            
            if answer:
                source = data.get('AbstractSource', 'DuckDuckGo')
                url = data.get('AbstractURL', '')
                
                output = f"Answer: {answer}\n\n"
                output += f"Source: {source}\n"
                if url:
                    output += f"More info: {url}"
                
                return ToolResult(success=True, output=output)
            else:
                return ToolResult(
                    success=False,
                    output="",
                    error="No instant answer found. Try web_search for more results."
                )
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error getting answer: {str(e)}"
            )
