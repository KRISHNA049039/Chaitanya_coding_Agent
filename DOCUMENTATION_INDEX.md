# 📚 Kiro Documentation Index

Welcome! This guide helps you navigate all Kiro documentation and get started quickly.

## 🚀 Start Here (Choose Your Path)

### Path 1: VS Code Extension (Recommended)
Best for: Interactive chat with beautiful UI, automatic history, keyboard shortcuts

1. **First 5 minutes**: [Quick Start Guide](QUICK_START_EXTENSION.md) ⚡
2. **Full reference**: [Extension Usage Guide](EXTENSION_USAGE_GUIDE.md) 📖
3. **Features overview**: [Extension Features](EXTENSION_FEATURES.md) 🎨

### Path 2: Command Line / Terminal
Best for: Scripting, automation, headless environments

1. **Getting started**: [Usage Guide](USAGE_GUIDE.md) 📖
2. **Example scripts**: [examples.py](examples.py) 💻
3. **Full app example**: [full_app_example.py](full_app_example.py) 🏗️

### Path 3: Advanced / Development
Best for: Custom tools, MCP servers, extending Kiro

1. **Architecture**: [Readme](README.md#features) 🏛️
2. **MCP integration**: [MCP Guide](MCP_GUIDE.md) 🔌
3. **Developer guide**: [Developer Cheatsheet](DEVELOPER_CHEATSHEET.md) ⚙️

---

## 📄 Complete File Manifest

### Getting Started
| File | Purpose | Read Time |
|------|---------|-----------|
| [QUICK_START_EXTENSION.md](QUICK_START_EXTENSION.md) | 5-minute VS Code setup | 5 min |
| [README.md](README.md) | Project overview & features | 10 min |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Command cheat sheet | 3 min |

### Extension Documentation
| File | Purpose | Read Time |
|------|---------|-----------|
| [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md) | Complete extension tutorial | 15 min |
| [EXTENSION_FEATURES.md](EXTENSION_FEATURES.md) | Features, workflows, customization | 10 min |
| [README_VS_CODE.md](README_VS_CODE.md) | VS Code task setup | 5 min |
| [kiro-vscode-extension/README.md](kiro-vscode-extension/README.md) | Extension technical details | 5 min |

### Usage & Examples
| File | Purpose | Read Time |
|------|---------|-----------|
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | CLI usage & Python API | 15 min |
| [VS_CODE_GUIDE.md](VS_CODE_GUIDE.md) | VS Code setup tips | 5 min |
| [examples.py](examples.py) | Code examples | 10 min |
| [full_app_example.py](full_app_example.py) | Complete app example | 10 min |

### Advanced Topics
| File | Purpose | Read Time |
|------|---------|-----------|
| [MCP_GUIDE.md](MCP_GUIDE.md) | Model Context Protocol setup | 15 min |
| [MCP_INTEGRATION_SUMMARY.md](MCP_INTEGRATION_SUMMARY.md) | MCP overview | 10 min |
| [DEVELOPER_CHEATSHEET.md](DEVELOPER_CHEATSHEET.md) | Developer quick reference | 5 min |

### Utilities & Benchmarks
| File | Purpose | Run Command |
|------|---------|-------------|
| [string_utils.py](string_utils.py) | Performance string helpers | `from string_utils import *` |
| [benchmarks/bench_strings.py](benchmarks/bench_strings.py) | String operation benchmarks | `python benchmarks/bench_strings.py` |

---

## 🎯 Common Tasks - Quick Links

### "I want to..."

| Task | Go To |
|------|-------|
| **Use the VS Code extension** | [QUICK_START_EXTENSION.md](QUICK_START_EXTENSION.md) |
| **Chat in the terminal** | [USAGE_GUIDE.md](USAGE_GUIDE.md) → Chat section |
| **Generate code** | [EXTENSION_FEATURES.md](EXTENSION_FEATURES.md) → Example Workflows |
| **Debug the extension** | [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md) → Troubleshooting |
| **Set up MCP servers** | [MCP_GUIDE.md](MCP_GUIDE.md) |
| **Write custom tools** | [DEVELOPER_CHEATSHEET.md](DEVELOPER_CHEATSHEET.md) |
| **Optimize string code** | `python benchmarks/bench_strings.py` |
| **See code examples** | [examples.py](examples.py) |
| **Check command syntax** | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |

---

## 🚀 Quick Start (30 seconds)

### Step 1: Prerequisites
```bash
ollama serve  # Start Ollama in one terminal
python --version  # Verify Python 3.8+
```

### Step 2: Install Extension
```bash
cd kiro-vscode-extension
npm install && npm run package
code --install-extension ./kiro-vscode-extension-*.vsix
```

### Step 3: Open Chat
Press **Ctrl+Shift+K** in VS Code

### Step 4: Start Chatting
Type: "Write a hello world Python script"

Done! 🎉

---

## 🗂️ Project Structure

```
Kiro/
├── agent.py                    # Main agent logic
├── cli.py                      # Command-line interface
├── config.py                   # Configuration loader
├── llm_client.py              # LLM integration (Ollama, etc.)
├── tools.py                   # Agent tools (execute_code, read_file, etc.)
├── mcp_client.py              # Model Context Protocol client
├── string_utils.py            # Performance string utilities
│
├── kiro-vscode-extension/     # VS Code extension
│   ├── extension.js           # Extension entry point
│   ├── package.json           # Manifest
│   ├── README.md              # Extension documentation
│   ├── build.sh/build.cmd     # Build scripts
│   └── .vscodeignore          # Packaging config
│
├── benchmarks/                # Performance benchmarks
│   └── bench_strings.py       # String operation benchmarks
│
├── .vscode/                   # VS Code workspace settings
│   ├── tasks.json             # Run tasks
│   └── kiro_chat_history/     # Chat history (auto-created)
│
├── examples.py                # Usage examples
├── full_app_example.py        # Complete application
│
└── Documentation files:
    ├── README.md              # Project overview
    ├── QUICK_START_EXTENSION.md
    ├── EXTENSION_USAGE_GUIDE.md
    ├── EXTENSION_FEATURES.md
    ├── USAGE_GUIDE.md
    ├── MCP_GUIDE.md
    ├── DEVELOPER_CHEATSHEET.md
    ├── VS_CODE_GUIDE.md
    ├── QUICK_REFERENCE.md
    ├── .env.example           # Environment template
    └── requirements.txt       # Python dependencies
```

---

## 🔗 External Resources

### LLM Services
- [Ollama](https://ollama.ai) - Local LLM runtime (recommended)
- [LM Studio](https://lmstudio.ai) - GUI for local LLMs
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - Lightweight C++ runtime
- [LocalAI](https://localai.io) - OpenAI-compatible API

### Models
- [Ollama Model Library](https://ollama.ai/library)
- [Hugging Face Models](https://huggingface.co/models)
- [OpenRouter](https://openrouter.ai) - API for various models

### VS Code
- [VS Code Extension API](https://code.visualstudio.com/api)
- [WebView Guide](https://code.visualstudio.com/api/extension-guides/webview)

---

## 💡 Tips

1. **Start simple**: Follow [QUICK_START_EXTENSION.md](QUICK_START_EXTENSION.md) first
2. **Keep it open**: Bookmark [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
3. **Explore examples**: Run [examples.py](examples.py) to see patterns
4. **Check status**: Run `python cli.py status` to verify setup
5. **Debug mode**: Use Ctrl+Shift+P → Developer: Toggle Developer Tools in the extension

---

## 📧 Need Help?

1. **Check the FAQ** in relevant guide (bottom of each file)
2. **Run troubleshooting**: `python cli.py setup`
3. **Verify setup**: `python cli.py status`
4. **Search docs**: Use Ctrl+F to search this index and files

---

## 🎓 Learning Path

**Beginner** (30 min)
1. [QUICK_START_EXTENSION.md](QUICK_START_EXTENSION.md)
2. [EXTENSION_FEATURES.md](EXTENSION_FEATURES.md)
3. [examples.py](examples.py)

**Intermediate** (1-2 hours)
1. [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md)
2. [USAGE_GUIDE.md](USAGE_GUIDE.md)
3. [MCP_GUIDE.md](MCP_GUIDE.md)

**Advanced** (2-4 hours)
1. [DEVELOPER_CHEATSHEET.md](DEVELOPER_CHEATSHEET.md)
2. [full_app_example.py](full_app_example.py)
3. [Agent architecture](README.md#architecture) (if present)

---

**Happy coding with Kiro! 🚀**
