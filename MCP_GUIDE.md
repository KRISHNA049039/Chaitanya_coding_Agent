# MCP (Model Context Protocol) Setup Guide

This guide explains how to set up and use Model Context Protocol (MCP) servers with Kiro.

## What is MCP?

The Model Context Protocol is a standardized way for AI models to interact with external tools and data sources. It allows Kiro to securely connect to different services and tools through a common interface.

## Quick Start with MCP

### 1. Using CLI to Add MCP Servers

```bash
# Add a GitHub MCP server
python cli.py mcp-add github "npx @modelcontextprotocol/server-github"

# Add a filesystem MCP server
python cli.py mcp-add filesystem "npx @modelcontextprotocol/server-filesystem"

# View all configured servers
python cli.py mcp-list

# Connect to a server
python cli.py mcp-connect github

# View available tools
python cli.py mcp-tools
```

### 2. Using Python API to Set Up MCP

```python
import asyncio
from agent import Agent
from config import MCPServerConfig

async def setup_mcp():
    agent = Agent()
    
    # Register an MCP server
    github_config = MCPServerConfig(
        name="github",
        command="npx @modelcontextprotocol/server-github",
        transport="stdio",
        env={"GITHUB_TOKEN": "your-github-token"}
    )
    
    agent.add_mcp_server(github_config)
    
    # Connect to the server
    success = await agent.connect_mcp_server("github")
    
    if success:
        print("Connected to GitHub MCP server!")
        
        # List available tools
        client = agent.mcp_manager.get_client("github")
        print("Available tools:")
        for tool_name in client.tools:
            print(f"  - {tool_name}")
    
    return agent

# Run the setup
agent = asyncio.run(setup_mcp())
```

## Popular MCP Servers

### GitHub MCP Server

Connect to GitHub to manage repositories, issues, pull requests, and more.

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-github
```

**Usage:**
```python
from config import MCPServerConfig

github_config = MCPServerConfig(
    name="github",
    command="npx @modelcontextprotocol/server-github",
    transport="stdio",
    env={"GITHUB_TOKEN": "ghp_xxxxx..."}
)
```

**Environment Variables:**
- `GITHUB_TOKEN` - Personal access token (required)

### Filesystem MCP Server

Access the local filesystem with security controls.

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Usage:**
```python
from config import MCPServerConfig

fs_config = MCPServerConfig(
    name="filesystem",
    command="npx @modelcontextprotocol/server-filesystem",
    transport="stdio",
    args=["--allowed-paths", "/home/user/documents"]
)
```

### PostgreSQL MCP Server

Query and manage PostgreSQL databases.

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-postgres
```

**Usage:**
```python
from config import MCPServerConfig

db_config = MCPServerConfig(
    name="postgres",
    command="npx @modelcontextprotocol/server-postgres",
    transport="stdio",
    env={
        "DATABASE_URL": "postgres://user:password@localhost/dbname"
    }
)
```

### Web Search MCP Server

Search the web for information.

**Installation:**
```bash
npm install -g @modelcontextprotocol/server-web-search
```

**Usage:**
```python
from config import MCPServerConfig

search_config = MCPServerConfig(
    name="web-search",
    command="npx @modelcontextprotocol/server-web-search",
    transport="stdio",
    env={"GOOGLE_API_KEY": "your-api-key"}
)
```

## Transport Types

### STDIO (Recommended)

Standard input/output communication - most common and secure.

```python
MCPServerConfig(
    name="my-server",
    command="python -m my_mcp_server",
    transport="stdio"  # or "stdio"
)
```

### HTTP

For servers running as HTTP services.

```python
MCPServerConfig(
    name="my-api",
    command="",  # Not needed
    transport="http",
    url="http://localhost:8000"
)
```

### WebSocket

For real-time bidirectional communication.

```python
MCPServerConfig(
    name="my-service",
    command="",  # Not needed
    transport="websocket",
    url="ws://localhost:8000"
)
```

## Creating Your Own MCP Server

### Python Example

```python
# my_mcp_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.tool()
def hello(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"

@server.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    server.run()
```

### Using Your Custom Server

```python
from config import MCPServerConfig
from agent import Agent
import asyncio

async def main():
    agent = Agent()
    
    config = MCPServerConfig(
        name="my-server",
        command="python my_mcp_server.py",
        transport="stdio"
    )
    
    agent.add_mcp_server(config)
    await agent.connect_mcp_server("my-server")
    
    # Now agent can use the tools

asyncio.run(main())
```

## Environment Variables Configuration

Add to `.env`:

```env
# Enable MCP
ENABLE_MCP=True

# Define MCP servers (format: name:command,name2:command2)
MCP_SERVERS=github:npx @modelcontextprotocol/server-github,filesystem:npx @modelcontextprotocol/server-filesystem

# MCP-specific env variables
GITHUB_TOKEN=ghp_xxxxx...
DATABASE_URL=postgres://user:password@localhost/db
```

## Auto-Connect to MCP Servers

Configure MCP servers in your config and they'll auto-connect on startup:

```python
from agent import Agent
import asyncio

async def main():
    agent = Agent()
    
    # Auto-connect to all enabled servers
    results = await agent.auto_connect_mcp_servers()
    
    for server_name, success in results.items():
        print(f"{server_name}: {'Connected' if success else 'Failed'}")

asyncio.run(main())
```

## Using MCP Tools in Agentic Loop

Once MCP servers are connected, Kiro automatically registers their tools and can use them:

```python
from agent import Agent
import asyncio

async def main():
    agent = Agent()
    
    # Register and connect to GitHub MCP
    from config import MCPServerConfig
    github_config = MCPServerConfig(
        name="github",
        command="npx @modelcontextprotocol/server-github",
        env={"GITHUB_TOKEN": "your-token"}
    )
    
    agent.add_mcp_server(github_config)
    await agent.connect_mcp_server("github")
    
    # Now the agent can use GitHub tools
    response = agent.run(
        "Create a GitHub issue titled 'Add validation' in my repo"
    )
    
    print(response)

asyncio.run(main())
```

## Security Considerations

### Token Management

Secure your API tokens and credentials:

```python
import os
from config import MCPServerConfig

github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable not set")

github_config = MCPServerConfig(
    name="github",
    command="npx @modelcontextprotocol/server-github",
    env={"GITHUB_TOKEN": github_token}
)
```

### Filesystem Access Control

Restrict filesystem access to specific paths:

```python
from config import MCPServerConfig

fs_config = MCPServerConfig(
    name="filesystem",
    command="npx @modelcontextprotocol/server-filesystem",
    args=[
        "--allowed-paths",
        "/home/user/documents",
        "/home/user/projects"
    ]
)
```

## Troubleshooting

### "Failed to connect to MCP server"

1. Check if the server command exists
```bash
which npx @modelcontextprotocol/server-github
```

2. Test the server manually
```bash
npx @modelcontextprotocol/server-github
```

3. Check environment variables are set
```bash
echo $GITHUB_TOKEN
```

### Tools not appearing after connection

1. List connected servers
```bash
python cli.py mcp-list
```

2. Check tools from specific server
```bash
python cli.py mcp-tools github
```

3. Verify in Python
```python
agent = Agent()
client = agent.mcp_manager.get_client("github")
print(client.tools if client else "Not connected")
```

### Connection timeout

Increase the timeout in config:

```python
agent.mcp_manager.call_tool(
    "github",
    "list_repos",
    {"username": "user"}
    # Timeout is handled via subprocess/http client settings
)
```

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Creating MCP Servers](https://modelcontextprotocol.io/docs/tools/creating)

---

Need help? Check the [main README](README.md) or open an issue!
