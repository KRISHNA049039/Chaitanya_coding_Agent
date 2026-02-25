# 🤖 Kiro - Local AI Agent with MCP Support

A powerful AI agent (inspired by GitHub Copilot) that runs completely locally with your own LLM model and supports the Model Context Protocol (MCP) for seamless tool integration. No cloud dependencies, full privacy, and complete control.

**Kiro** is an autonomous agent that can:
- 💬 Have intelligent conversations
- 🔧 Execute tools and perform tasks
- 💻 Generate and execute code
- 📁 Read and analyze files
- 🔌 Connect to MCP servers for extended functionality
- ⚡ Use an agentic loop for complex problem-solving
- 🎯 Reason through multi-step tasks

## 🚀 Get Started in 5 Minutes

→ **[Quick Start Guide](QUICK_START_EXTENSION.md)** - Install the VS Code extension and start chatting

→ **[Extension Usage Guide](EXTENSION_USAGE_GUIDE.md)** - Complete documentation for the extension

→ **[CLI Usage](USAGE_GUIDE.md)** - Terminal-based chat and advanced features

## Features

- **100% Local** - Runs on your machine with local LLM models (Ollama, llama.cpp, etc.)
- **No API Keys** - No need for OpenAI, Anthropic, or other cloud services
- **Privacy First** - Your data stays on your machine
- **MCP Integration** - Connect to Model Context Protocol servers for powerful tool ecosystems
- **CLI & Python API** - Use via command line or integrate into your code
- **Tool System** - Extensible tools for code execution, file operations, shell commands
- **Agentic Loop** - Multi-step reasoning and tool usage for complex tasks
- **Easy Setup** - Works with Ollama out of the box

## Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) or compatible LLM service running locally

### Installation

1. **Clone the repository**
```bash
cd /workspaces/Chaitanya_coding_Agent
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Ollama** (if not already installed)
```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai
```

4. **Start Ollama service**
```bash
ollama serve
```

5. **Pull a model** (in another terminal)
```bash
# Using Mistral (recommended, smaller)
ollama pull mistral

# Or other models:
ollama pull neural-chat
ollama pull llama2
ollama pull dolphin-mixtral
```

### Configuration

Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

Edit `.env`:
```env
LLM_MODEL_NAME=mistral
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
```

## Usage

### CLI Commands

**Start interactive chat:**
```bash
python cli.py chat
```

**Send a single message:**
```bash
python cli.py chat "How do I use Python decorators?"
```

**Generate code:**
```bash
python cli.py code "Write a function to validate email addresses"
```

**Check agent status:**
```bash
python cli.py status
```

**Setup and test:**
```bash
python cli.py setup
```

**MCP Server Commands:**

```bash
# List configured MCP servers
python cli.py mcp-list

# Add an MCP server
python cli.py mcp-add my-server "command to start server"

# Add HTTP-based MCP server
python cli.py mcp-add web-api --transport http --url http://localhost:8000

# Connect to an MCP server
python cli.py mcp-connect my-server

# List tools from connected MCP servers
python cli.py mcp-tools

# List tools from a specific server
python cli.py mcp-tools my-server
```

### Python API

**Basic chat:**
```python
from agent import Agent

agent = Agent()
response = agent.simple_chat("What is machine learning?")
print(response)
```

**Agentic loop with tools:**
```python
from agent import Agent

agent = Agent()
response = agent.run(
    "Write a Python script that calculates Fibonacci numbers and test it",
    verbose=True
)
print(response)
```

**Custom configuration:**
```python
from agent import Agent
from config import AgentConfig, LLMConfig

config = AgentConfig(
    llm_config=LLMConfig(
        model_name="neural-chat",
        temperature=0.5,
        max_tokens=1024,
    ),
    max_iterations=10,
)

agent = Agent(config=config)
response = agent.simple_chat("Your prompt here")
```

## Architecture

### Core Components

- **`agent.py`** - Main Agent class with agentic loop logic
- **`llm_client.py`** - Client for communicating with local LLM
- **`tools.py`** - Tool system for agent actions (code execution, file reading, shell commands)
- **`config.py`** - Configuration management
- **`cli.py`** - Command-line interface

### How It Works

```
User Input
    ↓
Agent receives input
    ↓
LLM generates response/decision
    ↓
Does response include tool use?
    ├─ Yes → Execute tool → Add result to conversation
    │         Go back to LLM
    └─ No  → Return response to user
```

## Supported Local LLMs

### Ollama (Recommended)
- Mistral (7B) - Fast and capable
- Neural Chat (7B)
- Llama 2 (7B, 13B)
- Dolphin Mixtral (8x7B)
- And many more...

### Other Compatible Services
- **LM Studio** - Beautiful UI for local models
- **llama.cpp** - Fast inference for GGUF models
- **LocalAI** - Open-source alternative to OpenAI

## Tools Available

### Built-in Tools

1. **execute_code** - Run Python code
```python
# The agent can use this internally
agent.run("Run this Python code: print('Hello')")
```

2. **read_file** - Read file contents
```python
agent.run("What's in the requirements.txt file?")
```

3. **execute_command** - Run shell commands
```python
agent.run("List all Python files in the current directory")
```

### MCP Tools

Kiro supports the **Model Context Protocol (MCP)** which allows you to connect to external tool providers and resources:

```python
from config import MCPServerConfig
from agent import Agent
import asyncio

agent = Agent()

# Add an MCP server
mcp_config = MCPServerConfig(
    name="github",
    command="npx @modelcontextprotocol/server-github",
    transport="stdio"
)
agent.add_mcp_server(mcp_config)

# Connect to the server
asyncio.run(agent.connect_mcp_server("github"))

# Now the agent can use tools from the MCP server
response = agent.run("Create a GitHub issue for me")
```

### Creating Custom Tools

```python
from tools import Tool, ToolResult

class MyCustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Description of what my tool does"
        )
    
    def execute(self, **kwargs) -> ToolResult:
        # Implement your tool logic here
        return ToolResult(success=True, output="Result")

# Register the tool
from agent import Agent
agent = Agent()
agent.tools.register(MyCustomTool())
```

## Examples

### Example 1: Code Generation
```bash
python cli.py code "Create a Python function to validate credit card numbers using Luhn algorithm"
```

### Example 2: Problem Solving
```bash
python cli.py chat "I have a Python list of dicts. How do I sort them by a specific key? Show me an example."
```

### Example 3: Multi-step Task
```python
from agent import Agent

agent = Agent()
response = agent.run("""
Create a Python script that:
1. Reads a CSV file
2. Filters rows where column 'age' > 18
3. Saves results to a new CSV file
4. Prints summary statistics
""", verbose=True)
```

## Model Recommendations

| Use Case | Recommended Model | Size |
|----------|------------------|------|
| **Fastest** | Mistral | 7B |
| **Balanced** | Neural Chat | 7B |
| **Smarter** | Dolphin Mixtral | 8x7B |
| **Quality** | Llama 2 | 13B |

## Troubleshooting

### "LLM service not available"
Make sure Ollama is running:
```bash
ollama serve
```

### "Model not found"
Pull the model first:
```bash
ollama pull mistral
```

### "Connection refused"
Check the LLM base URL in `.env`:
```env
LLM_BASE_URL=http://localhost:11434
```

### Slow responses
- Try a smaller model (Mistral)
- Reduce `LLM_MAX_TOKENS` in `.env`
- Check your system resources

## Performance

On a typical machine:
- **Mistral 7B** - ~5-10 responses/minute (CPU), ~30+ responses/minute (GPU)
- **Llama 2 13B** - ~2-5 responses/minute (CPU), ~15+ responses/minute (GPU)

For GPU acceleration with Ollama:
```
# NVIDIA GPU
ollama serve --gpus 1

# Apple Metal
# Automatically detected
```

## Development

### Project Structure
```
Chaitanya_coding_Agent/
├── agent.py           # Main agent logic with MCP support
├── llm_client.py      # LLM communication
├── mcp_client.py      # MCP client and server manager
├── tools.py           # Tool system with MCP integration
├── config.py          # Configuration with MCP setup
├── cli.py             # Command-line interface with MCP commands
├── examples.py        # Usage examples including MCP
├── requirements.txt   # Python dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

## MCP (Model Context Protocol) Integration

### What is MCP?

The Model Context Protocol (MCP) is a standard protocol that allows AI models to interact with external tools and data sources. Kiro integrates MCP to provide access to powerful and extensible tool ecosystems.

### How to Use MCP with Kiro

**1. Configure an MCP Server in Code:**

```python
from agent import Agent
from config import MCPServerConfig
import asyncio

agent = Agent()

# Register an MCP server
mcp_config = MCPServerConfig(
    name="github",
    command="npx @modelcontextprotocol/server-github",
    transport="stdio",  # or "http", "websocket"
    enabled=True
)
agent.add_mcp_server(mcp_config)

# Connect to the server
asyncio.run(agent.connect_mcp_server("github"))

# Agent can now use tools from the GitHub MCP server
response = agent.run("Create an issue on GitHub for me")
```

**2. Configure MCP Servers in .env:**

```env
# .env
ENABLE_MCP=True
MCP_SERVERS=github:npx @modelcontextprotocol/server-github,filesystem:npx @modelcontextprotocol/server-filesystem
```

**3. Use CLI to Manage MCP Servers:**

```bash
# Add a new MCP server
python cli.py mcp-add github "npx @modelcontextprotocol/server-github"

# View available MCP servers
python cli.py mcp-list

# Connect to an MCP server
python cli.py mcp-connect github

# View tools from MCP servers
python cli.py mcp-tools
```

### Supported MCP Transports

- **stdio** - Communication via standard input/output (most common)
- **http** - Communication via HTTP API (for remote servers)
- **websocket** - Communication via WebSocket (for real-time connections)

### Example MCP Servers

Here are some popular MCP servers you can use with Kiro:

| Server | Command | Use Case |
|--------|---------|----------|
| GitHub | `npx @modelcontextprotocol/server-github` | GitHub interaction |
| Filesystem | `npx @modelcontextprotocol/server-filesystem` | File operations |
| Postgres | `npx @modelcontextprotocol/server-postgres` | Database queries |
| Web Search | `npx @modelcontextprotocol/server-web-search` | Web searching |
| Slack | `npx @modelcontextprotocol/server-slack` | Slack integration |

### HTTP-Based MCP Server Example

For services running as HTTP servers:

```python
from config import MCPServerConfig

mcp_config = MCPServerConfig(
    name="my-api",
    command="",  # Not needed for HTTP
    transport="http",
    url="http://localhost:8000",
    enabled=True
)
```

### Advanced MCP Usage

```python
import asyncio
from agent import Agent
from config import MCPServerConfig

async def main():
    agent = Agent()
    
    # Register multiple MCP servers
    servers = [
        MCPServerConfig(
            name="github",
            command="npx @modelcontextprotocol/server-github",
            transport="stdio",
            env={"GITHUB_TOKEN": "your-token-here"}
        ),
        MCPServerConfig(
            name="filesystem",
            command="npx @modelcontextprotocol/server-filesystem",
            transport="stdio"
        )
    ]
    
    for config in servers:
        agent.add_mcp_server(config)
        success = await agent.connect_mcp_server(config.name)
        print(f"Connected to {config.name}: {success}")
    
    # List all available tools across all MCP servers
    all_tools = await agent.mcp_manager.list_all_tools()
    for server_name, tools in all_tools.items():
        print(f"\nTools from {server_name}:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool.get('description', 'N/A')}")
    
    # Run agent with access to MCP tools
    response = agent.run(
        "Use GitHub to create an issue, and use the filesystem to save the result"
    )
    print(f"\nAgent response: {response}")
    
    # Disconnect from servers
    await agent.mcp_manager.disconnect_all()

# Run
asyncio.run(main())
```

## Development

### Project Structure
```
Chaitanya_coding_Agent/
├── agent.py           # Main agent logic with MCP support
├── llm_client.py      # LLM communication
├── mcp_client.py      # MCP client and server manager
├── tools.py           # Tool system with MCP integration
├── config.py          # Configuration with MCP setup
├── cli.py             # Command-line interface with MCP commands
├── examples.py        # Usage examples including MCP
├── requirements.txt   # Python dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

### Running Examples
```bash
python examples.py
```

## VS Code Integration

### Kiro Chat Extension

A polished VS Code extension for interactive chat with your agent.

**Features:**
- 🎨 Beautiful WebView chat interface with timestamps and color-coded messages
- 💾 Automatic chat history persistence
- ⌨️ Keyboard shortcut: `Ctrl+Shift+K`
- 📝 Message formatting with role labels

**Quick Setup:**
```bash
cd kiro-vscode-extension
npm install
npm run package
```

Then install via VS Code Extensions → Install from VSIX.

See [kiro-vscode-extension/README.md](kiro-vscode-extension/README.md) for details.

## Performance & Utilities

### String Operations Benchmarks

Run benchmarks to compare string operation performance:

```bash
python benchmarks/bench_strings.py
```

Results show `''.join()` is ~30x faster than `+=`, and `str.translate()` is ~400x faster than regex for single-char replacement.

### String Utilities

Helper functions in `string_utils.py`:
- `StringBuilder`: Efficient string accumulation
- `fast_replace()`: Multi-string replacement
- `safe_split()`: Wrapper with edge-case handling
- `merge_lists_with_indices()`: O(n) merge avoiding `pop(0)`

## Contributing

Contributions welcome! Feel free to:
- Add new tools
- Improve the agent logic
- Add support for more LLM services
- Improve documentation

## License

MIT License - feel free to use in personal or commercial projects

## More Resources

- [Ollama Documentation](https://ollama.ai)
- [LM Studio](https://lmstudio.ai)
- [LocalAI](https://localai.io)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)

## Support

Need help? 
- Check the examples in `examples.py`
- Review the docstrings in the code
- Test with `python cli.py setup`

---

**Enjoy local, private AI! 🚀**
