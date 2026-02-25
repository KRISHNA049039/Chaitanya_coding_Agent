# Kiro Agent - VS Code Extension

AI coding agent with streaming chat and inline approvals, right in your VS Code sidebar!

## Features

✅ **Streaming Chat** - See responses in real-time  
✅ **Inline Approvals** - Approve/reject file changes with buttons  
✅ **Sidebar Panel** - Chat without leaving your editor  
✅ **Session Persistence** - Maintains conversation context  
✅ **Beautiful UI** - Matches VS Code theme  

## Installation

### 1. Build the Extension

```cmd
cd vscode-extension
npm install
npm run compile
```

### 2. Package the Extension

```cmd
npm run package
```

This creates `kiro-agent-0.1.0.vsix`

### 3. Install in VS Code

```cmd
code --install-extension kiro-agent-0.1.0.vsix
```

Or in VS Code:
1. Press `Ctrl+Shift+P`
2. Type "Install from VSIX"
3. Select the `.vsix` file

## Setup

### 1. Start the Agent Server

```cmd
cd Chaitanya_coding_Agent
python web_ui.py
```

### 2. Configure Extension

In VS Code settings (`Ctrl+,`):

```json
{
  "kiroAgent.serverUrl": "http://localhost:5000",
  "kiroAgent.modelName": "llama3.2:3b",
  "kiroAgent.enableStreaming": true
}
```

## Usage

### Open Chat Panel

1. Click the Kiro icon in the Activity Bar (left sidebar)
2. Or press `Ctrl+Shift+P` and type "Kiro: Open Chat"

### Chat with Agent

Type your message and press Enter or click Send.

Examples:
- "Create a Python hello world script"
- "Explain this code" (select code first)
- "Add error handling to this function"

### Approve Changes

When the agent proposes file changes, you'll see approval cards with:
- Operation type (create/modify/delete)
- File path
- Content preview
- **Approve** and **Reject** buttons

Click the buttons to approve or reject inline!

## Features in Detail

### Streaming Responses

Responses appear token-by-token as they're generated:
```
Agent: I'll create a Python script...
```

Much faster perceived response time!

### Inline Approvals

```
📋 Approval Required: change_1
Operation: create
Path: hello.py
Reason: Creating hello world script

Content:
print("Hello, World!")

[✓ Approve] [✗ Reject]
```

### Session Management

Each VS Code window has its own session. Conversation history is maintained automatically.

## Development

### Project Structure

```
vscode-extension/
├── package.json          # Extension manifest
├── src/
│   └── extension.ts      # Main extension code
├── tsconfig.json         # TypeScript config
└── README.md            # This file
```

### Build & Test

```cmd
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch mode (auto-compile)
npm run watch

# Package extension
npm run package
```

### Debug in VS Code

1. Open `vscode-extension` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the extension in the new window

## Configuration

### Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `kiroAgent.serverUrl` | `http://localhost:5000` | Agent server URL |
| `kiroAgent.modelName` | `llama3.2:3b` | LLM model name |
| `kiroAgent.enableStreaming` | `true` | Enable streaming |

### Commands

| Command | Description |
|---------|-------------|
| `Kiro: Open Chat` | Open chat panel |
| `Kiro: Clear Chat` | Clear conversation |

## Troubleshooting

### Extension Not Loading

Check VS Code Developer Tools:
1. `Help` → `Toggle Developer Tools`
2. Look for errors in Console

### Server Connection Failed

1. Make sure agent server is running:
   ```cmd
   python web_ui.py
   ```

2. Check server URL in settings

3. Test server manually:
   ```cmd
   curl http://localhost:5000/api/health
   ```

### Streaming Not Working

1. Enable streaming in settings:
   ```json
   "kiroAgent.enableStreaming": true
   ```

2. Check server supports streaming endpoint

## Comparison: Extension vs CLI vs Web UI

| Feature | Extension | CLI | Web UI |
|---------|-----------|-----|--------|
| Streaming | ✅ Yes | ✅ Yes | ❌ No |
| Inline Approvals | ✅ Yes | ⚠️ Terminal | ✅ Modal |
| IDE Integration | ✅ Perfect | ❌ No | ❌ No |
| Multi-window | ✅ Yes | ❌ No | ✅ Yes |
| Code Context | ✅ Auto | ❌ Manual | ❌ Manual |

## Roadmap

- [ ] Code selection context
- [ ] File tree integration
- [ ] Diff preview
- [ ] Multi-file edits
- [ ] Terminal integration
- [ ] Git integration

## License

MIT

---

**Enjoy coding with Kiro!** 🚀
