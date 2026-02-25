"""
Kiro AI Agent - Main Agent Logic
Integrates LLM, tools, MCP servers, and reasoning capabilities
"""
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import json
from datetime import datetime
import asyncio

from llm_client import LocalLLMClient, Message
from tools import ToolRegistry, create_default_registry
from config import AgentConfig, LLMConfig
from mcp_client import MCPServerManager, MCPServerConfig


class Agent:
    """Kiro AI Agent - Autonomous coding and problem-solving agent with MCP support"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize the agent
        
        Args:
            config: Agent configuration
        """
        self.config = config or AgentConfig()
        self.llm = LocalLLMClient(
            base_url=self.config.llm_config.base_url,
            model=self.config.llm_config.model_name,
            timeout=self.config.llm_config.timeout,
        )
        
        # Initialize approval handler for file operations
        from file_operations import approval_handler
        self.approval_handler = approval_handler
        
        # Create tools with approval handler
        self.tools = create_default_registry(approval_handler=self.approval_handler)
        self.conversation_history: List[Message] = []
        self.iteration_count = 0
        
        # Initialize MCP
        self.mcp_manager = MCPServerManager()
        self.tools.set_mcp_manager(self.mcp_manager)
        
        # Cache system prompt to avoid rebuilding
        self._system_prompt_cache = None
        
        # Check if LLM is available
        if not self.llm.is_available():
            raise RuntimeError(
                f"LLM service not available at {self.config.llm_config.base_url}\n"
                "Make sure you have Ollama running:\n"
                "  brew install ollama\n"
                "  ollama serve\n"
                f"  ollama pull {self.config.llm_config.model_name}"
            )
    
    def add_mcp_server(self, config: MCPServerConfig) -> None:
        """Register an MCP server"""
        self.mcp_manager.register_server(config)
    
    async def connect_mcp_server(self, server_name: str) -> bool:
        """Connect to an MCP server"""
        success = await self.mcp_manager.connect_server(server_name)
        
        if success:
            client = self.mcp_manager.get_client(server_name)
            if client:
                # Register MCP tools
                self.tools.register_mcp_tools(server_name, list(client.tools.values()))
        
        return success
    
    async def disconnect_mcp_server(self, server_name: str) -> bool:
        """Disconnect from an MCP server"""
        return await self.mcp_manager.disconnect_server(server_name)
    
    async def auto_connect_mcp_servers(self) -> Dict[str, bool]:
        """Auto-connect to enabled MCP servers from config"""
        results = {}
        for server_config in self.config.mcp_servers:
            if server_config.enabled:
                self.add_mcp_server(server_config)
                results[server_config.name] = await self.connect_mcp_server(server_config.name)
        return results
    
    def _build_system_prompt(self, force_rebuild: bool = False) -> str:
        """Build comprehensive system prompt with caching"""
        if self._system_prompt_cache and not force_rebuild:
            return self._system_prompt_cache
            
        # Simplified tool descriptions
        tool_list = []
        for name, tool in self.tools.tools.items():
            tool_list.append(f"- {name}: {tool.description}")
        
        tools_desc = '\n'.join(tool_list)
        
        system_prompt = f"""{self.config.llm_config.system_prompt}

Tools: {', '.join(self.tools.list_tools())}

Rules:
- "create file" → use create_file tool
- "modify file" → use modify_file tool
- "run/execute command" → use execute_shell tool
- "search web/internet" → use web_search tool
- "fetch/get URL" → use fetch_url tool
- "what is/quick answer" → use quick_answer tool
- Just explaining → respond normally

Format: {{"action": "use_tool", "tool_name": "tool_name", "arguments": {{"param": "value"}}}}

Examples:
File: {{"action": "use_tool", "tool_name": "create_file", "arguments": {{"path": "hello.txt", "content": "hello", "reason": "Create file"}}}}
Shell: {{"action": "use_tool", "tool_name": "execute_shell", "arguments": {{"command": "git status", "reason": "Check status"}}}}
Search: {{"action": "use_tool", "tool_name": "web_search", "arguments": {{"query": "Python tutorials", "num_results": 5}}}}
Fetch: {{"action": "use_tool", "tool_name": "fetch_url", "arguments": {{"url": "https://example.com"}}}}
Answer: {{"action": "use_tool", "tool_name": "quick_answer", "arguments": {{"query": "What is Python?"}}}}
"""
        self._system_prompt_cache = system_prompt
        return system_prompt
    
    def _parse_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse tool call from agent response"""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                try:
                    # Try to parse from this line onwards
                    json_str = '\n'.join(lines[i:])
                    data = json.loads(json_str)
                    if data.get("action") == "use_tool":
                        return data
                except json.JSONDecodeError:
                    continue
        return None
    
    def run(self, user_input: str, stream: bool = False, max_iterations: int = 3, verbose: bool = False):
        """
        Run agent with user input
        
        Args:
            user_input: User's message
            stream: Enable streaming responses
            max_iterations: Maximum iterations for agentic loop
            verbose: Enable verbose output
            
        Returns:
            Agent's response (string or generator if streaming)
        """
        if stream:
            # For streaming, use simple chat with streaming
            self.conversation_history = [Message(role="user", content=user_input)]
            
            return self.llm.chat(
                messages=self.conversation_history,
                temperature=self.config.llm_config.temperature,
                max_tokens=self.config.llm_config.max_tokens,
                system_prompt=self._build_system_prompt(),
                stream=True
            )
        else:
            # Use the main agentic loop logic (non-streaming)
            self.iteration_count = 0
            self.conversation_history = []
            
            # Add user message
            self.conversation_history.append(Message(role="user", content=user_input))
            
            if verbose:
                print(f"\n{'='*60}")
                print(f"🤖 Kiro Agent Starting")
                print(f"{'='*60}")
                print(f"User: {user_input}\n")
            
            while self.iteration_count < max_iterations:
                self.iteration_count += 1
                
                if verbose:
                    print(f"--- Iteration {self.iteration_count} ---")
                
                # Get response from LLM
                if verbose:
                    print("Agent: ", end="", flush=True)
                
                response = self.llm.chat(
                    messages=self.conversation_history,
                    temperature=self.config.llm_config.temperature,
                    max_tokens=self.config.llm_config.max_tokens,
                    system_prompt=self._build_system_prompt(),
                    stream=False,
                )
                
                if verbose:
                    print(response[:200] + "..." if len(response) > 200 else response)
                
                # Add assistant response to history
                self.conversation_history.append(Message(role="assistant", content=response))
                
                # Check if tool call is needed
                tool_call = self._parse_tool_call(response)
                
                if tool_call:
                    tool_name = tool_call.get("tool_name")
                    arguments = tool_call.get("arguments", {})
                    
                    if verbose:
                        print(f"[TOOL] Using tool: {tool_name}")
                        print(f"   Arguments: {arguments}")
                    
                    # Execute tool
                    result = self.tools.execute(tool_name, **arguments)
                    
                    if verbose:
                        print(f"   Result: {result.output[:100] if result.output else result.error}")
                    
                    # Add tool result to conversation
                    tool_response = f"Tool '{tool_name}' executed. "
                    if result.success:
                        tool_response += f"Output: {result.output}"
                    else:
                        tool_response += f"Error: {result.error}"
                    
                    self.conversation_history.append(
                        Message(role="user", content=f"[Tool Result]\n{tool_response}")
                    )
                else:
                    # No tool call needed, agent is done
                    if verbose:
                        print(f"\n{'='*60}")
                        print(f"✅ Kiro Agent Complete")
                        print(f"{'='*60}\n")
                    
                    return response
            
            # Max iterations reached
            if verbose:
                print(f"\n⚠️  Max iterations ({max_iterations}) reached")
            
            return response
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_name": self.config.llm_config.agent_name,
            "model": self.config.llm_config.model_name,
            "llm_url": self.config.llm_config.base_url,
            "tools": self.tools.list_tools(),
            "mcp_servers_connected": self.mcp_manager.list_connected_servers(),
            "mcp_servers_available": self.mcp_manager.list_available_servers(),
            "conversation_length": len(self.conversation_history),
            "last_iteration": self.iteration_count,
            "timestamp": datetime.now().isoformat(),
        }
