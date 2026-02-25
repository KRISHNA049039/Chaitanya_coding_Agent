"""
Local LLM Client - Handles communication with local LLM models
Supports Ollama and compatible APIs
"""
from typing import Optional, List, Dict, Any
import requests
from dataclasses import dataclass
import json


@dataclass
class Message:
    """Represents a chat message"""
    role: str  # "user", "assistant", "system"
    content: str


class LocalLLMClient:
    """Client for interacting with local LLM models"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral", timeout: int = 120):
        """
        Initialize LLM client
        
        Args:
            base_url: Base URL of the LLM API (default: Ollama)
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.chat_endpoint = f"{self.base_url}/api/chat"
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"LLM service unavailable: {e}")
            return False
    
    def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        stream: bool = False,
    ):
        """
        Send chat request to local LLM
        
        Args:
            messages: List of messages in conversation
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            system_prompt: System prompt to use
            stream: Enable streaming responses
            
        Returns:
            Generated response from LLM (string if not streaming, generator if streaming)
        """
        # Build message list
        formatted_messages = []
        
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": temperature,
            "stream": stream,
        }
        
        if max_tokens:
            payload["options"] = {
                "num_predict": max_tokens
            }
        
        try:
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                # Return generator for streaming
                def stream_generator():
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                if "message" in chunk:
                                    content = chunk["message"].get("content", "")
                                    full_response += content
                                    yield content
                                # Check if done
                                if chunk.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                return stream_generator()
            else:
                result = response.json()
                return result.get("message", {}).get("content", "")
        
        except requests.exceptions.Timeout:
            raise RuntimeError(f"LLM request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"Failed to connect to LLM at {self.base_url}")
        except requests.exceptions.HTTPError as e:
            # More detailed error for HTTP errors
            raise RuntimeError(f"LLM HTTP error: {e}. Check if model '{self.model}' exists. Try: ollama pull {self.model}")
        except Exception as e:
            raise RuntimeError(f"LLM request failed: {str(e)}")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text from a prompt (non-chat mode)
        
        Args:
            prompt: Input prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        return self.chat(
            messages=[Message(role="user", content=prompt)],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    def list_models(self) -> List[str]:
        """List available models on the LLM service"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            
            data = response.json()
            models = data.get("models", [])
            return [m.get("name") for m in models if "name" in m]
        except Exception as e:
            print(f"Failed to list models: {e}")
            return []
