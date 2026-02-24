# Kiro with MCP - Quick Reference

## Installation

```bash
cd /workspaces/Chaitanya_coding_Agent
pip install -r requirements.txt
cp .env.example .env
```

## Start Local LLM

```bash
# Install Ollama
brew install ollama

# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull mistral
```

## CLI Commands - Quick Reference

### Basic Agent Commands
```bash
python cli.py chat                          # Interactive chat
python cli.py chat "your prompt"            # Single message
python cli.py code "write a function"       # Code generation
python cli.py status                        # Check status
python cli.py setup                         # Setup & test
```

### MCP Commands
```bash
python cli.py mcp-list                      # List MCP servers
python cli.py mcp-add name "command"        # Add MCP server
python cli.py mcp-connect name              # Connect to server
python cli.py mcp-tools                     # List all MCP tools
python cli.py mcp-tools server-name         # List server tools
```

## Python API - Quick Reference

### Basic Usage
```python
from agent import Agent

agent = Agent()
response = agent.simple_chat("Hello!")
print(response)
```

### With MCP
```python
import asyncio
from agent import Agent
from config import MCPServerConfig

async def main():
    agent = Agent()
    
    # Register MCP server
    mcp_config = MCPServerConfig(
        name="github",
        command="npx @modelcontextprotocol/server-github",
        env={"GITHUB_TOKEN": "your-token"}
    )
    
    agent.add_mcp_server(mcp_config)
    await agent.connect_mcp_server("github")
    
    # Use agent with MCP tools
    response = agent.run("Create a GitHub issue")
    print(response)

asyncio.run(main())
```

### Agentic Loop
```python
agent = Agent()
response = agent.run(
    "Your complex task here",
    verbose=True  # See agent thinking
)
```

## MCP Server Examples

### GitHub
```bash
python cli.py mcp-add github "npx @modelcontextprotocol/server-github"
# Requires: GITHUB_TOKEN env variable
```

### Filesystem
```bash
python cli.py mcp-add filesystem "npx @modelcontextprotocol/server-filesystem"
```

### PostgreSQL
```bash
python cli.py mcp-add postgres "npx @modelcontextprotocol/server-postgres"
# Requires: DATABASE_URL env variable
```

### Web Search
```bash
python cli.py mcp-add search "npx @modelcontextprotocol/server-web-search"
# Requires: GOOGLE_API_KEY env variable
```

## Configuration (.env)

```env
# LLM Settings
LLM_MODEL_NAME=mistral              # or: neural-chat, llama2, dolphin-mixtral
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.7                 # 0.0=deterministic, 1.0=creative
LLM_MAX_TOKENS=2048

# MCP Settings
ENABLE_MCP=True
GITHUB_TOKEN=ghp_xxxxx...
DATABASE_URL=postgres://...
```

## File Guide

| File | Purpose |
|------|---------|
| `agent.py` | Main Agent class with MCP support |
| `mcp_client.py` | MCP server client & manager |
| `llm_client.py` | LLM API communication |
| `tools.py` | Tool registry and execution |
| `config.py` | Configuration management |
| `cli.py` | Command-line interface |
| `examples.py` | Usage examples |
| `README.md` | Full documentation |
| `MCP_GUIDE.md` | MCP-specific guide |

## Troubleshooting

### LLM Not Available
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull a model
ollama pull mistral
```

### MCP Connection Failed
```bash
# Check if command exists
npx @modelcontextprotocol/server-github --version

# Test connection
python cli.py mcp-connect github

# View detailed errors
DEBUG=True python cli.py mcp-connect github
```

### Tools Not Showing
```bash
# List connected servers
python cli.py mcp-list

# View tools from specific server
python cli.py mcp-tools github

# Check in Python
from agent import Agent
agent = Agent()
print(agent.tools.list_tools())
```

## Common Workflows

### Workflow 1: Interactive Chat with Tools
```bash
python cli.py setup                    # Verify setup
python cli.py mcp-add github "..."     # Add MCP server
python cli.py mcp-connect github       # Connect
python cli.py chat                     # Start chatting
```

### Workflow 2: Code Generation + File Management
```python
import asyncio
from agent import Agent
from config import MCPServerConfig

async def main():
    agent = Agent()
    
    # Setup filesystem access
    fs_config = MCPServerConfig(
        name="filesystem",
        command="npx @modelcontextprotocol/server-filesystem"
    )
    agent.add_mcp_server(fs_config)
    await agent.connect_mcp_server("filesystem")
    
    # Generate and save code
    code = agent.run(
        "Generate a Python function to sort a list and save it"
    )

asyncio.run(main())
```

### Workflow 3: Multi-Server Complex Task
```python
async def setup_multiple_servers():
    configs = [
        MCPServerConfig(name="github", command="..."),
        MCPServerConfig(name="filesystem", command="..."),
    ]
    
    for config in configs:
        agent.add_mcp_server(config)
        await agent.connect_mcp_server(config.name)
    
    # Now agent can use tools from all servers
    response = agent.run(
        "Create a GitHub repo, add code, and commit"
    )
```

## Performance Tips

1. **Use smaller models for speed**: Mistral (7B) is fastest
2. **Enable GPU**: `export CUDA_VISIBLE_DEVICES=0`
3. **Reduce tokens**: Set `LLM_MAX_TOKENS=1024` for faster responses
4. **Cache MCP tools**: Connect once, reuse agent instance
5. **Batch operations**: Combine multiple operations in one prompt

## Security

1. **Never commit .env**: Use `.env.example` as template
2. **Protect tokens**: Use environment variables, not hardcoded
3. **Limit filesystem access**: Use `--allowed-paths` with filesystem MCP
4. **Validate commands**: Don't execute arbitrary commands from untrusted sources

## Resources

- **Main README**: `README.md` - Complete documentation
- **MCP Guide**: `MCP_GUIDE.md` - MCP server setup & usage
- **Examples**: `examples.py` - Working code examples
- **CLI Help**: `python cli.py --help` - Command reference
- **MCP Official**: https://modelcontextprotocol.io/

---

**Quick Links:**
- 🚀 Get Started: `python cli.py setup`
- 💬 Chat: `python cli.py chat`
- 🔌 Add MCP: `python cli.py mcp-add name "command"`
- 📚 Docs: `README.md` or `MCP_GUIDE.md`
