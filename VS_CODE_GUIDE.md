# Running Kiro in VS Code

VS Code has built-in support for running and debugging Kiro. Follow these guides for different use cases.

## ⚡ Quick Start

### 1. Install Required Extensions
Open VS Code's Extension Marketplace (Ctrl+Shift+X) and install:
- **Python** (ms-python.python) - Required for Python support
- **Pylance** (ms-python.vscode-pylance) - For smart code completion
- **Black Formatter** (ms-python.black-formatter) - Code formatting

### 2. Setup Python Environment (Optional but Recommended)

```bash
# In VS Code Terminal (Ctrl+`)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Kiro

**Option A: Using Tasks (Recommended)**
- Press `Ctrl+Shift+P` and search "Run Task"
- Select a Kiro task:
  - `Kiro: Chat` - Interactive chat
  - `Kiro: Setup` - Setup and test
  - `Kiro: Status` - Check status
  - `Kiro: MCP List` - List MCP servers

**Option B: Using Launch/Debug (F5)**
- Press `F5` or click Run → Start Debugging
- Select a Kiro configuration:
  - `Kiro - Interactive Chat`
  - `Kiro - Setup & Test`
  - `Kiro - Check Status`
  - `Kiro - Custom Chat` (edit args at bottom)

**Option C: Using Terminal**
```bash
# In VS Code Terminal (Ctrl+`)
python cli.py chat
python cli.py setup
python cli.py code "write a function"
```

## 📋 Available Tasks

### Kiro Agent Tasks
| Task | Command | Use Case |
|------|---------|----------|
| Chat | `python cli.py chat` | Interactive conversation |
| Setup | `python cli.py setup` | Verify installation |
| Status | `python cli.py status` | Check agent status |
| Code Generation | `python cli.py code "..."` | Generate code |
| Run Examples | `python examples.py` | See usage examples |

### MCP Tasks
| Task | Command | Use Case |
|------|---------|----------|
| MCP List | `python cli.py mcp-list` | List MCP servers |
| MCP Tools | `python cli.py mcp-tools` | View available tools |

### Setup Tasks
| Task | Command | Use Case |
|------|---------|----------|
| Install Dependencies | `pip install -r requirements.txt` | Install packages |
| Ollama: Start | `ollama serve` | Start Ollama service |
| Ollama: Pull Mistral | `ollama pull mistral` | Download model |

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Open Command Palette → Run Task |
| `F5` | Start Debugging (Launch from .vscode/launch.json) |
| `Ctrl+`` | Toggle Integrated Terminal |
| `Ctrl+J` | Focus Terminal |
| `Ctrl+Shift+T` | Kill Terminal |

## 🔧 Run & Debug Configurations

### Debug Configuration (F5)
Pre-configured debug launches in `.vscode/launch.json`:

```json
{
    "name": "Kiro - Interactive Chat",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/cli.py",
    "console": "integratedTerminal",
    "args": ["chat"]
}
```

To create a custom configuration:
1. Press `F5` → "Create a launch.json file"
2. Select "Python" environment
3. Add custom configurations

### Task Configuration (Ctrl+Shift+P)
Pre-configured tasks in `.vscode/tasks.json`:

```json
{
    "label": "Kiro: Chat",
    "type": "shell",
    "command": "python",
    "args": ["cli.py", "chat"],
    "presentation": {
        "reveal": "always",
        "focus": true,
        "panel": "shared"
    }
}
```

## 🔍 Debugging Tips

### Add Breakpoint
1. Click on line number to add a red dot
2. Press `F5` to start debugging
3. Step through code with F10 (step over) or F11 (step into)

### View Variables
- Click "Debug" tab on left sidebar
- Expand "Variables" section to see current values

### Run Code in Debug Console
1. Hit breakpoint in debugger
2. Press `Ctrl+Shift+D` to focus Debug Console
3. Type Python commands to inspect state

### Example Debugging Session
```python
# cli.py
from agent import Agent

agent = Agent()  # ← Set breakpoint here (F9)
response = agent.simple_chat("Hello")  # ← Step over (F10)
print(response)  # ← Step into (F11)
```

## 📖 Workspace Structure in VS Code

```
.vscode/
├── launch.json          # Debug configurations
├── tasks.json           # Runnable tasks
├── settings.json        # Workspace settings
└── extensions.json      # Recommended extensions

agent.py                 # Main agent code
cli.py                   # CLI interface
mcp_client.py           # MCP support
```

## 🚀 Common Workflows

### Workflow 1: Interactive Development
1. Open integrated terminal: `Ctrl+``
2. Activate venv: `source venv/bin/activate`
3. Run task: `Ctrl+Shift+P` → "Kiro: Chat"
4. Modify code while running
5. Restart with same task

### Workflow 2: Debug Agent Logic
1. Open `agent.py` in editor
2. Click line number to add breakpoint
3. Press `F5` → Select "Kiro - Interactive Chat"
4. Execute step-by-step with F10/F11
5. Inspect variables in Debug tab

### Workflow 3: Test Code Generation
1. Press `Ctrl+Shift+P` → "Kiro: Code Generation"
2. View output in terminal
3. Modify `cli.py` code generation prompt
4. Run again to see changes

### Workflow 4: Setup & Deploy
1. Terminal: `Ctrl+``
2. Run task: `Ollama: Start Service` (background)
3. Run task: `Ollama: Pull Mistral`
4. Run task: `Kiro: Setup`
5. Run task: `Kiro: Chat`

## 🔌 MCP Development in VS Code

### Monitor MCP Connections
1. Open integrated terminal: `Ctrl+``
2. Run: `python cli.py mcp-list`
3. Run: `python cli.py mcp-tools`

### Debug MCP Tool Calls
1. Open `agent.py`
2. Find `_parse_tool_call` method
3. Add breakpoint before tool execution
4. Run: `F5` → "Kiro - Interactive Chat"
5. Step through tool execution

### Test MCP Server
```bash
# Terminal (Ctrl+`)
python cli.py mcp-add test-server "python -m my_mcp_server"
python cli.py mcp-connect test-server
python cli.py mcp-tools test-server
```

## 🐛 Troubleshooting

### "Python not found"
- Press `Ctrl+Shift+P` → "Python: Select Interpreter"
- Choose Python path or venv

### "Ollama not running"
- Run task: `Ollama: Start Service`
- Or manually: `ollama serve` in terminal

### "LLM service not available"
- Check: `python cli.py setup`
- Pull model: Run task "Ollama: Pull Mistral"

### "Module not found"
- Run task: "Install Dependencies"
- Or manually: `pip install -r requirements.txt`

### Tasks not showing
- Click `Ctrl+Shift+P` → "Tasks: Rerun Last Task"
- Or manually define in `.vscode/tasks.json`

## 📚 Tips & Tricks

### Run Previous Task Again
- Press `Ctrl+Shift+P` → "Tasks: Rerun Last Task"

### Stop Running Task
- Press `Ctrl+C` in terminal or click stop button

### View Task Output
- Terminal appears automatically when task runs
- Click "Terminal" tab to view output

### Create Custom Task
1. Press `Ctrl+Shift+P` → "Tasks: Open User Task"
2. Add new task configuration:
```json
{
    "label": "My Custom Task",
    "type": "shell",
    "command": "python",
    "args": ["your_script.py"],
    "presentation": {
        "reveal": "always",
        "focus": true
    }
}
```

### Set Default Build Task
1. Right-click any task
2. Select "Mark as Default Build Task"
3. Press `Ctrl+Shift+B` to run it

## 🎓 Learning Resources

### Inside VS Code
- **Integrated Help**: `Ctrl+Shift+P` → "Help: Welcome"
- **Python Tutorial**: `Ctrl+Shift+P` → "Welcome: Open"
- **Debugger Guide**: [MS Python Debugging](https://code.visualstudio.com/docs/python/debugging)

### External Resources
- [VS Code Python Guide](https://code.visualstudio.com/docs/languages/python)
- [Task Runner Documentation](https://code.visualstudio.com/docs/editor/tasks)
- [Debugging Guide](https://code.visualstudio.com/docs/editor/debugging)

---

**Quick Help:**
- Tasks: `Ctrl+Shift+P` → "Run Task"
- Debug: `F5`
- Terminal: `Ctrl+``
- Command Palette: `Ctrl+Shift+P`
