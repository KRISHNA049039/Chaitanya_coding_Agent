# 💬 CLI Chat Interface

Interactive command-line chat with streaming responses!

## Quick Start

```cmd
cd Chaitanya_coding_Agent
.venv\Scripts\activate
python cli_chat.py
```

## Features

✅ **Streaming Responses** - See agent thinking in real-time  
✅ **Color-Coded Output** - Easy to read  
✅ **File Approval** - Approve/reject changes inline  
✅ **MCP Integration** - All MCP tools available  
✅ **Session Management** - Persistent conversation  

## Commands

### Chat Commands

- `/help` - Show help message
- `/clear` - Clear conversation history
- `/tools` - List available tools
- `/exit` - Exit chat

### Approval Commands

- `approve change_1` - Approve pending file change
- `reject change_1` - Reject pending file change

## Example Session

```
🚀 Initializing Kiro Agent...
🔌 Connecting MCP servers...
✓ Agent ready!

============================================================
  🤖 Kiro Agent - CLI Chat
============================================================
Model: llama3.2:3b
Session: 833efe0b...

You: Create a hello.py file

Agent: I'll create a Python file for you...

📋 APPROVAL REQUIRED: change_1
============================================================
Operation: create
Path: hello.py
Reason: Creating hello world script

Content:
print("Hello, World!")

Commands:
  approve change_1 - Approve this change
  reject change_1 - Reject this change
============================================================

You: approve change_1

✓ Created file: hello.py

Agent: File created successfully!

You: /exit
👋 Goodbye!
```

## Advantages Over Web UI

1. **Faster** - No browser overhead
2. **Streaming** - See responses as they generate
3. **Lightweight** - Terminal only
4. **Scriptable** - Can pipe input/output
5. **Better for coding** - Stay in terminal workflow

## Color Coding

- 🟢 **Green** - User input, success messages
- 🔵 **Cyan** - Agent responses, system info
- 🟡 **Yellow** - Warnings, approval requests
- 🔴 **Red** - Errors

## Tips

### Quick Approvals

When agent proposes changes, you'll see:
```
📋 APPROVAL REQUIRED: change_1
```

Just type:
```
approve change_1
```

### Multiple Pending Changes

List pending changes:
```
You: /tools
```

Approve all at once:
```
approve change_1
approve change_2
approve change_3
```

### Faster Model

For quicker responses in CLI:
```env
LLM_MODEL_NAME=llama3.2:3b
LLM_TIMEOUT=180
```

### Debug Mode

Enable debug output:
```env
DEBUG=True
```

## Comparison: CLI vs Web UI

| Feature | CLI | Web UI |
|---------|-----|--------|
| Speed | ⚡ Fast | 🐢 Slower |
| Streaming | ✅ Yes | ❌ No |
| File Approval | ✅ Inline | ✅ Modal |
| MCP Tools | ✅ Yes | ✅ Yes |
| History | ✅ Session | ✅ Database |
| Multi-user | ❌ No | ✅ Yes |
| Mobile | ❌ No | ✅ Yes |

## Troubleshooting

### Colors Not Working

Windows users need colorama:
```cmd
pip install colorama
```

### Agent Timeout

Increase timeout in `.env`:
```env
LLM_TIMEOUT=300
```

### MCP Servers Not Connecting

Check MCP configuration:
```cmd
python cli_chat.py
```

Look for connection errors in startup.

## Advanced Usage

### Pipe Input

```cmd
echo "Create a README.md" | python cli_chat.py
```

### Redirect Output

```cmd
python cli_chat.py > session.log
```

### Background Mode

```cmd
python cli_chat.py &
```

## Integration with IDE

### VS Code Terminal

1. Open integrated terminal (Ctrl+`)
2. Run `python cli_chat.py`
3. Chat while coding!

### Kiro IDE

Already integrated! Just use the terminal panel.

---

**Enjoy faster, streamlined agent interactions!** 🚀
