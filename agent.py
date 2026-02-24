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
        self.tools = create_default_registry()
        self.conversation_history: List[Message] = []
        self.iteration_count = 0
        
        # Initialize MCP
        self.mcp_manager = MCPServerManager()
        self.tools.set_mcp_manager(self.mcp_manager)
        
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
    
    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt"""
        tools_desc = self.tools.get_tools_description()
        mcp_info = ""
        
        if self.mcp_manager.list_connected_servers():
            mcp_info = f"\n\nConnected MCP Servers: {', '.join(self.mcp_manager.list_connected_servers())}"
        
        system_prompt = f"""{self.config.llm_config.system_prompt}

Available Tools:
{tools_desc}{mcp_info}

Tool Usage Format:
When you need to use a tool, format your response as JSON on a new line:
{{
  "action": "use_tool",
  "tool_name": "tool_name",
  "arguments": {{"param": "value"}}
}}

After tool execution, analyze the result and continue with your next action.

Current Status:
- Agent: {self.config.llm_config.agent_name}
- Model: {self.config.llm_config.model_name}
- Tools: {', '.join(self.tools.list_tools())}
"""
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
    
    def run(
        self,
        user_input: str,
        max_iterations: Optional[int] = None,
        verbose: bool = False,
    ) -> str:
        """
        Run the agent in an agentic loop
        
        Args:
            user_input: User's request
            max_iterations: Max iterations (default from config)
            verbose: Print detailed output
            
        Returns:
            Final response from agent
        """
        max_iterations = max_iterations or self.config.max_iterations
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
            response = self.llm.chat(
                messages=self.conversation_history,
                temperature=self.config.llm_config.temperature,
                max_tokens=self.config.llm_config.max_tokens,
                system_prompt=self._build_system_prompt(),
            )
            
            if verbose:
                print(f"Agent: {response[:200]}...")
            
            # Add assistant response to history
            self.conversation_history.append(Message(role="assistant", content=response))
            
            # Check if tool call is needed
            tool_call = self._parse_tool_call(response)
            
            if tool_call:
                tool_name = tool_call.get("tool_name")
                arguments = tool_call.get("arguments", {})
                
                if verbose:
                    print(f"🔧 Using tool: {tool_name}")
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
    
    def simple_chat(self, user_input: str) -> str:
        """
        Simple one-turn chat (no agentic loop)
        
        Args:
            user_input: User's message
            
        Returns:
            Agent's response
        """
        self.conversation_history = [Message(role="user", content=user_input)]
        
        response = self.llm.chat(
            messages=self.conversation_history,
            temperature=self.config.llm_config.temperature,
            max_tokens=self.config.llm_config.max_tokens,
            system_prompt=self.config.llm_config.system_prompt,
        )
        
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
