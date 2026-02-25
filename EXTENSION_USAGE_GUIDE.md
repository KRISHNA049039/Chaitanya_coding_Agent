# Kiro Chat Extension - Complete Usage Guide

This guide covers everything you need to know about using the Kiro Chat extension in VS Code.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Features & UI](#features--ui)
4. [Chat Interface](#chat-interface)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Chat History](#chat-history)
7. [Running Tasks](#running-tasks)
8. [Troubleshooting](#troubleshooting)
9. [Development Mode](#development-mode)

---

## Installation

### Option A: From VSIX (Pre-packaged)

1. **Download the VSIX file** (pre-built or after building locally)
2. **Open VS Code**
3. Go to Extensions (Ctrl+Shift+X)
4. Click the **⋯ (More Actions)** button
5. Select **Install from VSIX...**
6. Navigate to and select the `.vsix` file
7. VS Code will install the extension automatically

### Option B: Build Locally

1. **Open a terminal** in the `kiro-vscode-extension` folder:
   ```bash
   cd kiro-vscode-extension
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the VSIX**:
   ```bash
   npm run package
   ```

4. **Install the generated file**:
   ```bash
   code --install-extension ./kiro-vscode-extension-0.1.0.vsix
   ```

5. **Reload VS Code** (Ctrl+Shift+P → Developer: Reload Window)

### Option C: Development Mode (F5)

1. Open the workspace in VS Code
2. Navigate to the `kiro-vscode-extension` folder
3. Press **F5** to launch the Extension Development Host
4. A new VS Code window will open with the extension active

---

## Quick Start

### 1. Prerequisites

Ensure you have:
- ✅ **Ollama running** locally (`http://localhost:11434`)
  - Start with: `ollama serve`
  - Install a model: `ollama pull llama3.1:8b`
- ✅ **Python 3.8+** on your PATH
- ✅ **`.env` file** in the workspace root with:
  ```
  LLM_MODEL_NAME=llama3.1:8b
  LLM_BASE_URL=http://localhost:11434
  LLM_TEMPERATURE=0.7
  LLM_MAX_TOKENS=2048
  ```

### 2. Start the Chat

Press **`Ctrl+Shift+K`** (Windows/Linux) or **`Cmd+Shift+K`** (Mac)

Or use the Command Palette:
- Press **Ctrl+Shift+P** (Cmd+Shift+P on Mac)
- Type `Kiro: Start Chat`
- Press Enter

A WebView panel will open on the right side of your editor.

### 3. Start Chatting

1. Click in the **message input box** (bottom of the panel)
2. **Type a message** (e.g., "Write a hello world Python script")
3. Press **Enter** to send
4. Wait for the agent to respond

---

## Features & UI

### Message Display

Each message shows:
- **Role**: User, Agent, System, or Error (color-coded)
- **Text**: The actual message content (monospace font for readability)
- **Timestamp**: When the message was sent/received (HH:MM:SS)

### Color Scheme

| Role | Color | Background |
|------|-------|-----------|
| User | Green | Dark green tint |
| Agent | Blue | Dark gray |
| Error | Red | Dark red tint |
| System | Cyan | Dark gray |

### Buttons

| Button | Action |
|--------|--------|
| **Send** | Send the typed message to the agent |
| **Stop** | Kill the agent process immediately |

---

## Chat Interface

### Sending Messages

1. **Type** in the input box
2. Press **Enter** or click **Send**
3. Your message appears as a "User" message with a timestamp
4. The agent processes and responds

### Receiving Responses

- Agent responses appear as **"Agent"** messages
- Large responses are displayed with smooth scrolling
- Errors appear as red **"Error"** messages
- System messages (start/stop) appear in cyan

### Multi-line Messages

Currently, pressing **Enter** sends the message. Shift+Enter is not yet implemented (can add later).

**Workaround**: Copy/paste multi-line text, or split into separate messages.

---

## Keyboard Shortcuts

| Shortcut | Action | Platform |
|----------|--------|----------|
| **Ctrl+Shift+K** | Open/Focus Kiro Chat | Windows/Linux |
| **Cmd+Shift+K** | Open/Focus Kiro Chat | Mac |
| **Enter** | Send message | All |
| **Ctrl+Shift+P** | Open Command Palette | Windows/Linux |
| **Cmd+Shift+P** | Open Command Palette | Mac |

### Custom Commands

In the Command Palette, you can also run:
- `Kiro: Start Chat` — Opens the chat panel
- `Tasks: Run Task` — Run the CLI task (if configured)

---

## Chat History

### Automatic Saving

Chat history is automatically saved when the agent process exits. Files are saved to:
```
.vscode/kiro_chat_history/chat_<timestamp>.json
```

Example path:
```
.vscode/kiro_chat_history/chat_1708858320000.json
```

### History Format

Each file is a JSON array of message objects:
```json
[
  {
    "role": "user",
    "text": "Write a hello world script",
    "timestamp": "14:30:45"
  },
  {
    "role": "agent",
    "text": "```python\nprint('Hello, World!')\n```",
    "timestamp": "14:30:47"
  }
]
```

### Viewing History

1. **Open File Explorer** (Ctrl+Shift+E)
2. Navigate to `.vscode/kiro_chat_history/`
3. Click any `chat_*.json` file to view
4. History is read-only JSON format (can be copied/analyzed)

---

## Running Tasks

### Using the Integrated Task

You can also run the agent from the VS Code integrated terminal using the configured task:

1. Press **Ctrl+Shift+P** and search for `Tasks: Run Task`
2. Select `Run Kiro Chat`
3. The terminal will start the interactive CLI chat

**This is useful if you prefer the terminal over the WebView.**

### Or Run Manually

```bash
python cli.py chat
```

---

## Troubleshooting

### "LLM service not available"

**Problem**: The extension shows an error about the LLM service.

**Solution**:
1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```
2. Verify the LLM_BASE_URL in `.env`:
   ```
   LLM_BASE_URL=http://localhost:11434
   ```
3. Check that the model is installed:
   ```bash
   ollama pull llama3.1:8b
   ```

### "Python not found"

**Problem**: The extension can't find Python.

**Solution**:
1. Ensure Python is on your PATH:
   ```bash
   python --version
   ```
2. If not, add Python to PATH or use the full path in settings

### Extension won't activate

**Problem**: "Kiro: Start Chat" command doesn't appear.

**Solution**:
1. Reload VS Code: Ctrl+Shift+P → Developer: Reload Window
2. Check that the extension is installed:
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Kiro"
   - Ensure it shows as "Installed"

### Messages not sending

**Problem**: Typed messages aren't being sent to the agent.

**Solution**:
1. Check the agent is running:
   - Look for "Agent process exited" message
   - Click "Start Chat" again to restart
2. Click **Stop**, then start a new chat

### Chat history not saving

**Problem**: History files aren't created in `.vscode/kiro_chat_history/`.

**Solution**:
1. The directory is auto-created; just ensure you have write permissions
2. Close the chat gracefully (click Stop or close the panel)
3. Wait a moment for the file to be written

---

## Development Mode

### Testing Changes

If you're modifying the extension:

1. **Make your changes** to `extension.js` or the WebView HTML/CSS
2. Press **Ctrl+Shift+F5** to reload the Extension Development Host
3. Test in the new window
4. Debug using the Debug Console (View → Debug Console)

### Logging

Add `console.log()` statements in `extension.js`:
```javascript
console.log('Agent started with PID:', agentProc.pid);
```

These will appear in the Debug Console.

### Debugging WebView

1. In the Extension Development Host, press **Ctrl+Shift+P**
2. Search for `Developer: Open Webview Developer Tools`
3. Use browser DevTools to inspect HTML/CSS and debug JavaScript

---

## Tips & Tricks

### 1. Complex Requests

For multi-step tasks, provide context in one message:
```
Write a Python script that:
1. Reads a CSV file
2. Filters rows where age > 18
3. Outputs to a new CSV

Use pandas if needed.
```

### 2. Code Review

Ask the agent to review or optimize code:
```
Review this function for performance issues:

def merge_sort(arr):
    ...
```

### 3. Continuous Learning

Ask follow-up questions:
```
Can you explain how merge sort works?
What's the time complexity?
How does it compare to quicksort?
```

### 4. Mix Commands

The agent can execute code, run shell commands, and provide explanations:
```
Generate a test suite for my function and run it
```

---

## Keyboard Remapping (Optional)

Don't like `Ctrl+Shift+K`? You can remap it:

1. Open VS Code Settings (Ctrl+,)
2. Search for `Keyboard Shortcuts`
3. Click "Open Keyboard Shortcuts (JSON)"
4. Add:
   ```json
   {
     "key": "ctrl+alt+k",
     "command": "kiro.startChat"
   }
   ```

---

## Support & Feedback

### Common Questions

**Q: Can I use a different LLM service?**
- Yes! Edit `.env` to change `LLM_BASE_URL` (e.g., LM Studio, llama.cpp)

**Q: Is my chat history private?**
- Yes! Everything stays in `.vscode/` on your machine. No cloud upload.

**Q: Can I export chat history?**
- Yes, the JSON files in `.vscode/kiro_chat_history/` can be backed up or analyzed

**Q: Can I use multiple chat sessions?**
- Yes! Each session creates a new chat panel, but only one agent runs at a time (previous ones stop)

### Need Help?

1. Check [kiro-vscode-extension/README.md](kiro-vscode-extension/README.md)
2. Review [USAGE_GUIDE.md](USAGE_GUIDE.md) for general Kiro usage
3. Check agent logs: `python cli.py status`

---

## Next Steps

- Explore **string utilities** for performance tips: `python benchmarks/bench_strings.py`
- Run the **CLI chat** for terminal-based interactions: `python cli.py chat`
- Check **MCP integration** for extended tools: `python cli.py mcp-list`

Enjoy your local AI agent! 🚀
