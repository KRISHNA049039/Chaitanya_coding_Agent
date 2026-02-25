# Kiro Chat - VS Code Extension

Kiro Chat brings your local AI agent directly into VS Code. Chat with your Kiro agent, execute code, and run commands all from a beautiful WebView interface.

## Features

- 🤖 **Live Chat Interface**: Clean, modern chat UI with timestamps and message formatting
- 💾 **Persistent History**: Automatically saves chat history to `.vscode/kiro_chat_history/`
- ⌨️ **Keyboard Shortcuts**: Press `Ctrl+Shift+K` (Cmd+Shift+K on Mac) to open Kiro Chat
- 🎨 **Syntax Highlighting**: Color-coded messages for different roles (user, agent, system, error)
- 🔌 **Seamless Integration**: Runs the existing `python cli.py chat` agent in the background

## Requirements

- VS Code 1.60+
- Python 3.8+
- Ollama running locally (`http://localhost:11434`)
- Kiro agent files (`cli.py`, `agent.py`, etc.) in the workspace root

## Installation

### Option 1: Install from VSIX (Prepackaged)
1. Download the `.vsix` file
2. In VS Code: Extensions → More Actions (⋯) → Install from VSIX
3. Select the file and install

### Option 2: Development Mode
1. Open this extension folder in VS Code
2. Press `F5` to launch the Extension Development Host
3. In the dev host, run `Kiro: Start Chat` from the Command Palette

## Usage

1. **Start Chat**: Press `Ctrl+Shift+K` or run `Kiro: Start Chat` from the Command Palette
2. **Type Messages**: Send messages to the agent; it will execute code, run commands, or provide answers
3. **Stop Agent**: Click the `Stop` button to kill the agent process
4. **View History**: Chat history is saved to `.vscode/kiro_chat_history/chat_*.json`

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+K | Open Kiro Chat |
| Enter | Send message |
| Shift+Enter | New line (not implemented yet) |

## Troubleshooting

- **"LLM service not available"**: Ensure Ollama is running (`ollama serve`)
- **"Module not found"**: Ensure Python is on PATH and the workspace root contains `cli.py`
- **Extension won't activate**: Check that the workspace root is the Kiro agent project folder

## Packaging

To create a VSIX file:

```bash
cd kiro-vscode-extension
npm install
npm run package
```

This generates `kiro-vscode-extension-0.1.0.vsix`, which you can share or install via the Extension menu.

To publish to the VS Code Marketplace:

```bash
npm run publish
```

(Requires a publisher account on the VS Code Marketplace.)

## Development

The extension uses:
- **extension.js**: Main extension logic, spawns the agent process, manages WebView communication
- **package.json**: Manifest, keybindings, and build configuration
- **HTML/CSS/JS in getWebviewContent()**: UI rendering and message handling

### Messages Saved

Chat history is automatically saved after the agent process exits to:
```
.vscode/kiro_chat_history/chat_<timestamp>.json
```

Each message object includes `{ role, text, timestamp }`.

