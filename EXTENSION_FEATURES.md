# Kiro Chat Extension - Feature Summary

## 🎨 Visual Chat Interface

Beautiful, modern WebView chat with:
- ✨ **Color-coded messages** (User=Green, Agent=Blue, Error=Red, System=Cyan)
- ⏰ **Precise timestamps** on every message
- 📜 **Auto-scrolling** to latest messages
- 🎭 **Role labels** for clarity
- 💾 **Automatic history saving** to JSON files

## ⌨️ Keyboard & Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+Shift+K** | Open/toggle Kiro Chat panel |
| **Cmd+Shift+K** | macOS equivalent |
| **Enter** | Send message |
| **Ctrl+Shift+P** | Command Palette (search commands) |

## 🚀 Quick Actions

**From Command Palette (Ctrl+Shift+P):**
- Type `Kiro: Start Chat` → Opens the extension
- Type `Tasks: Run Task` → Run CLI chat in integrated terminal
- Type `Developer: Reload Window` → Reload extension (dev mode)

## 📊 Chat History

**Auto-saved to:**
```
.vscode/kiro_chat_history/chat_<timestamp>.json
```

**Format:**
```json
[
  { "role": "user", "text": "...", "timestamp": "14:30:45" },
  { "role": "agent", "text": "...", "timestamp": "14:30:47" }
]
```

**Access:**
- File Explorer → .vscode → kiro_chat_history
- View, copy, or analyze anytime

## 🔧 Supported Features

The agent can:
- ✅ **Execute Python code** (shows output in real-time)
- ✅ **Run shell commands** (bash, PowerShell, etc.)
- ✅ **Read files** from the workspace
- ✅ **Generate code** with explanations
- ✅ **Explain code** and provide optimizations
- ✅ **Reason through** multi-step problems
- ✅ **Use MCP servers** (if configured)

## 🎯 Example Workflows

### Workflow 1: Code Generation
```
You: "Create a Python function to calculate Fibonacci numbers"
    ↓
Agent: Writes code + explanation
    ↓
You: "Add unit tests for this function"
    ↓
Agent: Generates tests + runs them
```

### Workflow 2: Code Review
```
You: [Paste your code] "Review this for performance issues"
    ↓
Agent: Analyzes + suggests optimizations
    ↓
You: "Implement the suggestions and show me the diff"
    ↓
Agent: Updates code + shows changes
```

### Workflow 3: Learning
```
You: "Explain how merge sort works"
    ↓
Agent: Explains algorithm
    ↓
You: "What's the time complexity?"
    ↓
Agent: Detailed analysis
    ↓
You: "Show me an implementation"
    ↓
Agent: Code + walkthrough
```

## 🏆 Why Use the Extension?

| Feature | CLI (`python cli.py chat`) | Extension (WebView) |
|---------|---------------------------|-------------------|
| **Chat Interface** | Terminal | Beautiful WebView |
| **History** | Requires manual save | Auto-saved JSON |
| **Code Display** | Plain text | Formatted code blocks |
| **Integration** | ✓ Works | ✓ Works + VS Code context |
| **Keyboard Shortcuts** | Limited | Full VS Code support |
| **UI Polish** | Basic | Professional |

Both work great—pick based on preference!

## 🛠️ Customization

### Change Keyboard Shortcut

1. Ctrl+K Ctrl+S (Open Keyboard Shortcuts)
2. Search `kiro.startChat`
3. Double-click and set new shortcut (e.g., `Ctrl+Alt+K`)

### Change LLM Model

Edit `.env`:
```dotenv
LLM_MODEL_NAME=mistral:latest
# Then: ollama pull mistral:latest
```

### Adjust Temperature (Creativity)

Edit `.env`:
```dotenv
LLM_TEMPERATURE=0.9  # More creative (0.0-1.0)
LLM_MAX_TOKENS=4096  # Longer responses
```

## 📈 Performance Tips

For faster responses:
- Use smaller models: `mistral:latest`, `neural-chat:latest`
- Reduce `LLM_MAX_TOKENS` for shorter responses
- Use quantized models (Q4 or Q5 variants)

For longer context:
- Increase `LLM_MAX_TOKENS` (uses more memory)
- Use larger models: `llama3.1:70b` (requires GPU)

## 🐛 Debugging

### View Extension Logs
1. Ctrl+Shift+P → Developer: Toggle Developer Tools
2. Check Console tab for errors

### Check Agent Status
```bash
python cli.py status
```

### Verify LLM Service
```bash
curl http://localhost:11434/api/tags
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [QUICK_START_EXTENSION.md](QUICK_START_EXTENSION.md) | 5-minute setup |
| [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md) | Complete guide (this file) |
| [README.md](README.md) | Project overview |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | CLI usage |
| [MCP_GUIDE.md](MCP_GUIDE.md) | Advanced MCP servers |

## 🎓 Learning Resources

**String Performance:**
```bash
python benchmarks/bench_strings.py
```
Compare `join()` vs `+=`, `str.translate()` vs regex, etc.

**String Utilities:**
```python
from string_utils import StringBuilder, fast_replace, merge_lists_with_indices
```

## 🆘 Troubleshooting Checklist

- [ ] Ollama running? (`ollama serve`)
- [ ] LLM model installed? (`ollama list`)
- [ ] `.env` file exists with correct URL?
- [ ] Python on PATH? (`python --version`)
- [ ] Extension installed? (Check Extensions sidebar)
- [ ] VS Code reloaded? (Ctrl+Shift+P → Reload Window)

## 🚀 Next Level

Once comfortable:
1. Configure **MCP servers** for extended tools
2. Create **custom tools** in `tools.py`
3. Use the **Python API** for automation
4. Build **workflows** combining agent + your scripts

## 💡 Pro Tips

1. **Paste large code blocks** directly into messages
2. **Ask for explanations** after code is generated
3. **Save important chats** by copying the JSON history
4. **Chain requests**: "Now optimize this" or "Add error handling"
5. **Use specific prompts**: "Explain like I'm a beginner" works better than vague requests

---

**You're all set! Press `Ctrl+Shift+K` and start chatting. 🚀**
