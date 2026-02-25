# Kiro Chat - Quick Start (5 Minutes)

## Step 1: Prerequisites ✅

```bash
# Check Python is installed
python --version

# Start Ollama (in a separate terminal)
ollama serve

# In another terminal, ensure the model is installed
ollama pull llama3.1:8b
```

## Step 2: Setup Environment 🔧

In the workspace root, create/verify `.env` file:
```dotenv
LLM_MODEL_NAME=llama3.1:8b
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
```

## Step 3: Install Extension 📦

### Option A: From Pre-built VSIX
```bash
code --install-extension ./kiro-vscode-extension-0.1.0.vsix
```

### Option B: Build Locally
```bash
cd kiro-vscode-extension
npm install
npm run package
code --install-extension ./kiro-vscode-extension-0.1.0.vsix
```

### Option C: Development Mode (F5)
- Open `kiro-vscode-extension` folder
- Press **F5**

## Step 4: Open Chat 💬

Press **`Ctrl+Shift+K`** (Windows/Linux) or **`Cmd+Shift+K`** (Mac)

Or: Ctrl+Shift+P → `Kiro: Start Chat`

## Step 5: Start Typing! 🚀

```
Example 1: "Write a hello world Python script"
Example 2: "What is the time complexity of merge sort?"
Example 3: "Create a function to validate email addresses"
```

Press **Enter** to send.

---

## Common Tasks

### Task: Generate Code
```
You: "Write a function to calculate factorial"
```

### Task: Explain Code
```
You: "Explain how this sorting algorithm works [paste code]"
```

### Task: Debug
```
You: "This function isn't working. What's wrong? [paste code]"
```

### Task: Performance Tips
```
You: "How can I make this string operation faster?"
```

---

## UI Overview

```
┌─────────────────────────────────────┐
│  💬 Kiro Chat                       │
├─────────────────────────────────────┤
│                                     │
│ User: Write hello world          💚 │ (green)
│ 14:30:45                            │
│                                     │
│ Agent: Here's a Python script:   💙 │ (blue)
│ ```python                           │
│ print("Hello, World!")              │
│ ```                                 │
│ 14:30:47                            │
│                                     │
├─────────────────────────────────────┤
│ [Input box: Type message...]        │
│ [Send] [Stop]                       │
└─────────────────────────────────────┘
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+Shift+K** | Open Kiro Chat |
| **Enter** | Send message |
| **Ctrl+Shift+P** | Command Palette |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "LLM not available" | Ensure Ollama is running: `ollama serve` |
| "Python not found" | Add Python to PATH or use full path |
| Extension won't load | Reload: Ctrl+Shift+P → Developer: Reload Window |
| Agent crashed | Click Stop, then start a new chat |

---

## Where to Go From Here

📖 **Full Guide**: [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md)

⚡ **Performance Tips**: `python benchmarks/bench_strings.py`

🔌 **Advanced MCP Setup**: [MCP_GUIDE.md](MCP_GUIDE.md)

🎮 **Terminal Chat**: `python cli.py chat`

---

**That's it! You're ready to chat with your local AI agent. 🎉**
