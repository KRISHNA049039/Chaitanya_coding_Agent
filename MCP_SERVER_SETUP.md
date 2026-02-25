# 🔌 MCP Server Setup for Kiro IDE

Use your agent directly in Kiro IDE's chat interface!

## Setup Steps

### 1. Test the MCP Server

First, make sure it works:

```cmd
cd Chaitanya_coding_Agent
python mcp_server_wrapper.py
```

Then type (press Enter after each line):
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

You should see JSON responses. Press `Ctrl+C` to stop.

### 2. Configure Kiro IDE

#### Option A: Workspace Configuration (Recommended)

Create `.kiro/settings/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "my-kiro-agent": {
      "command": "python",
      "args": ["C:/Users/AKIN/OneDrive/Documents/my_coding_agent/Chaitanya_coding_Agent/mcp_server_wrapper.py"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Important:** Use the FULL absolute path to `mcp_server_wrapper.py`!

#### Option B: User Configuration (Global)

Edit `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "my-kiro-agent": {
      "command": "python",
      "args": ["C:/Users/AKIN/OneDrive/Documents/my_coding_agent/Chaitanya_coding_Agent/mcp_server_wrapper.py"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### 3. Restart Kiro IDE

Close and reopen Kiro IDE, or:
1. Press `Ctrl+Shift+P`
2. Type "Reload Window"
3. Press Enter

### 4. Verify Connection

In Kiro IDE:
1. Press `Ctrl+Shift+P`
2. Type "MCP"
3. Look for "MCP Server" commands
4. Check if "my-kiro-agent" is listed

Or check the MCP panel in the sidebar.

### 5. Use Your Agent!

Now you can chat with your agent in Kiro IDE:

```
@my-kiro-agent chat with message "Create a Python hello world script"
```

Or just:
```
Create a Python hello world script
```

And Kiro IDE will route it to your agent!

## Available Tools

Your agent exposes these MCP tools:

### 1. chat
Chat with your agent - supports all features:
- Code generation
- File operations (with approval)
- Web searches
- Shell commands
- PDF reading
- Vector search

**Example:**
```
@my-kiro-agent chat with message "Search the web for Python best practices"
```

### 2. get_status
Get agent status and available tools

**Example:**
```
@my-kiro-agent get_status
```

## Troubleshooting

### Server Not Connecting

1. Check logs in Kiro IDE Developer Tools:
   - `Help` → `Toggle Developer Tools`
   - Look for MCP errors

2. Test server manually:
   ```cmd
   python mcp_server_wrapper.py
   ```
   Type: `{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}`

3. Check Python path:
   ```cmd
   where python
   ```

### Wrong Python Version

If using virtual environment:
```json
{
  "mcpServers": {
    "my-kiro-agent": {
      "command": "C:/Users/AKIN/OneDrive/Documents/my_coding_agent/Chaitanya_coding_Agent/.venv/Scripts/python.exe",
      "args": ["mcp_server_wrapper.py"],
      "env": {},
      "disabled": false
    }
  }
}
```

### Dependencies Missing

Make sure all dependencies are installed:
```cmd
cd Chaitanya_coding_Agent
pip install -r requirements.txt
```

Or with uv:
```cmd
uv sync
```

### Logs Not Showing

Check stderr output. MCP servers log to stderr, not stdout.

## Advanced Configuration

### Auto-Approve Tools

To skip approval for certain tools:
```json
{
  "mcpServers": {
    "my-kiro-agent": {
      "command": "python",
      "args": ["mcp_server_wrapper.py"],
      "autoApprove": ["chat", "get_status"]
    }
  }
}
```

### Environment Variables

Pass environment variables:
```json
{
  "mcpServers": {
    "my-kiro-agent": {
      "command": "python",
      "args": ["mcp_server_wrapper.py"],
      "env": {
        "LLM_MODEL_NAME": "llama3.2:3b",
        "DEBUG": "True"
      }
    }
  }
}
```

### Multiple Instances

Run multiple agents:
```json
{
  "mcpServers": {
    "agent-fast": {
      "command": "python",
      "args": ["mcp_server_wrapper.py"],
      "env": {"LLM_MODEL_NAME": "gemma2:2b"}
    },
    "agent-smart": {
      "command": "python",
      "args": ["mcp_server_wrapper.py"],
      "env": {"LLM_MODEL_NAME": "llama3.1:8b"}
    }
  }
}
```

## Usage Examples

### Code Generation
```
@my-kiro-agent chat with message "Create a FastAPI REST API with CRUD operations"
```

### File Operations
```
@my-kiro-agent chat with message "Create a Dockerfile for this Python project"
```

### Web Search
```
@my-kiro-agent chat with message "Search for the latest Python 3.12 features"
```

### Status Check
```
@my-kiro-agent get_status
```

## Benefits

✅ **Integrated** - Chat directly in Kiro IDE  
✅ **Streaming** - See responses in real-time  
✅ **Context-Aware** - Agent has access to your workspace  
✅ **Approvals** - File operations require approval  
✅ **Persistent** - Conversation history maintained  

## Next Steps

1. Test the MCP server
2. Configure Kiro IDE
3. Restart IDE
4. Start chatting!

---

**Your agent is now part of Kiro IDE!** 🎉
