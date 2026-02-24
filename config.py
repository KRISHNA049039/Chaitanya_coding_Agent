"""
Local LLM and MCP Configuration
"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class MCPServerConfig(BaseModel):
    """MCP Server Configuration"""
    name: str = Field(description="Unique name for the MCP server")
    command: str = Field(description="Command to start the server (for stdio)")
    transport: str = Field(default="stdio", description="Transport type: stdio, http, websocket")
    url: Optional[str] = Field(default=None, description="Base URL for HTTP/WebSocket servers")
    args: List[str] = Field(default_factory=list, description="Additional arguments for the command")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    enabled: bool = Field(default=True, description="Whether to auto-connect on startup")


class LLMConfig(BaseModel):
    """Configuration for Local LLM"""
    
    # Ollama Configuration
    model_name: str = Field(default="mistral", description="Model name to use")
    base_url: str = Field(default="http://localhost:11434", description="Base URL for LLM API")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=2048, description="Maximum tokens to generate")
    timeout: int = Field(default=120, description="Request timeout in seconds")
    
    # Agent Configuration
    agent_name: str = Field(default="Kiro", description="Name of the agent")
    system_prompt: str = Field(default="""You are Kiro, an advanced AI coding agent. You help users with:
- Code development and debugging
- Technical problem-solving
- Architecture and design decisions
- Best practices and optimization

Be concise, direct, and provide actionable solutions.
When using tools or executing code, explain your approach clearly.""")
    
    # Tool Configuration
    enable_tools: bool = Field(default=True, description="Enable tool usage")
    tools_timeout: int = Field(default=30, description="Tool execution timeout")


class AgentConfig(BaseModel):
    """Agent Configuration"""
    
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    mcp_servers: List[MCPServerConfig] = Field(default_factory=list, description="MCP server configurations")
    max_iterations: int = Field(default=10, description="Maximum iterations for agent loop")
    debug: bool = Field(default=False, description="Enable debug mode")
    enable_mcp: bool = Field(default=True, description="Enable MCP integration")


def load_config() -> AgentConfig:
    """Load configuration from environment or defaults"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Load MCP servers from environment
    mcp_servers = []
    # Example: MCP_SERVERS=server1:command,server2:command
    mcp_servers_env = os.getenv("MCP_SERVERS", "")
    
    return AgentConfig(
        llm_config=LLMConfig(
            model_name=os.getenv("LLM_MODEL_NAME", "mistral"),
            base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
        ),
        enable_mcp=os.getenv("ENABLE_MCP", "True").lower() == "true",
        mcp_servers=mcp_servers,
        debug=os.getenv("DEBUG", "False").lower() == "true"
    )
