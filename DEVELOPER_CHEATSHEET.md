<!-- START_KIRO_CHEATSHEET -->
# Kiro - Developer Cheatsheet

## 🚀 TL;DR - How to Use Kiro to Build Apps

```bash
# 1. Start Kiro once (keep it running)
python cli.py chat

# 2. Work in other terminals
npm start          # Your app dev server
npm run build      # Your build commands

# 3. Ask Kiro for help in the chat
# Type your questions in Kiro's chat (Terminal 1)
# It stays running the whole time!

# 4. Copy generated code into your app
# Build, test, iterate
```

**That's it!** You don't close Kiro - you keep it running as your coding assistant.

---

## 📋 Common Questions & Answers

### Q: Do I need to run Kiro every time?
**A:** No! Start it once with `python cli.py chat` and keep it running. Use the same chat session for all your questions.

### Q: Can I switch projects?
**A:** Yes! You can ask Kiro about different projects in the same chat. Example:
```
> "I'm working on Project A, frontend code for..."
> [work on Project A]
> "Now let me work on Project B, backend for..."
> [work on Project B]
```

### Q: What if my terminal closes?
**A:** Just run `python cli.py chat` again. You'll start a fresh session, but all your previous conversations are stored.

### Q: Can I use Kiro with my existing code?
**A:** Absolutely! Just ask Kiro to review, debug, or improve your existing code.

---

## 🎯 Workflow Templates

### Template 1: Start New Project
```
Terminal 1: python cli.py chat
  > "I need a [framework] project for [purpose]"
  > "Generate basic structure for..."
  > "Add authentication..."
  > "Add database models..."

Terminal 2: Set up your project with generated code
Terminal 3: npm start (or your dev server)

Keep asking Kiro in Terminal 1 as you develop!
```

### Template 2: Debug Existing Code
```
Terminal 1: python cli.py chat
  > "I'm getting this error: [paste error]"
  > Kiro gives solution
  > "Can you explain why?"
  > Kiro explains

Terminal 2: Apply fix to your code
Terminal 3: Test the fix
```

### Template 3: Add Feature
```
Terminal 1: python cli.py chat
  > "Generate [feature] using [technology]"
  > "Make it handle [requirement]"
  > "How do I integrate this with [existing code]?"
  
Terminal 2: Copy code and integrate
Terminal 3: Test new feature
```

---

## 💬 Useful Prompts

### Code Generation
```
"Generate a [language] function to [task]"
"Create a [framework] component for [purpose]"
"Write a database migration that [does something]"
"Generate an API endpoint for [functionality]"
```

### Debugging
```
"I'm getting this error: [error message]. Fix it: [code]"
"Why is this [language] code not working? [code]"
"Debug this bug: [description]"
"My [technology] code is slow. Optimize it: [code]"
```

### Learning
```
"Explain how [technology/concept] works"
"Show me best practices for [technology]"
"What's the difference between [A] and [B]?"
"How do I do [task] in [language]?"
```

### Code Review
```
"Review this code for bugs: [code]"
"Suggest improvements for this code: [code]"
"Is this secure? [code]"
"How can I make this code better? [code]"
```

### Architecture
```
"I want to build [app]. What's the best architecture?"
"Should I use [A] or [B] for this project?"
"How should I structure my [type] application?"
```

---

## ⌨️ VS Code Integration

### Run via Tasks
```
Ctrl+Shift+P → "Run Task" → Pick "Kiro: Chat"
```

### Run via Terminal
```
Ctrl+` (backtick) → python cli.py chat
```

### Debug with Breakpoints
```
F5 → Select "Kiro - Interactive Chat"
Click line number to add breakpoint
Step through code with F10/F11
```

---

## 📱 Real-World Examples

### Building a Web App
```
Step 1: python cli.py chat
Step 2: Ask for backend boilerplate
Step 3: Ask for frontend component
Step 4: Ask for API integration code
Step 5: Ask for deployment instructions
Done!
```

### Building a CLI Tool
```
Step 1: python cli.py chat
Step 2: Ask for Click/Typer CLI structure
Step 3: Ask for specific commands
Step 4: Ask for error handling
Step 5: Ask for testing approach
Done!
```

### Building a Data Processing Script
```
Step 1: python cli.py chat
Step 2: Ask for data loading code
Step 3: Ask for processing logic
Step 4: Ask for optimization
Step 5: Ask for output formatting
Done!
```

---

## 🔧 Terminal Setup (Recommended)

```
Terminal 1: python cli.py chat        ← Keep running
           (Ask Kiro all your questions here)

Terminal 2: npm start (or your dev)  ← Your main dev server
           
Terminal 3: npm test (or builds)     ← Testing/builds

Terminal 4: git commands, etc         ← Git/file operations
```

---

## 🚀 Quick Commands

```bash
# Start interactive chat
python cli.py chat

# Quick code generation
python cli.py code "write a function to do X"

# Setup and test
python cli.py setup

# Check status
python cli.py status

# View available tools
python cli.py mcp-tools

# Add MCP server
python cli.py mcp-add name "command"

# Run in VS Code
F5 or Ctrl+Shift+P → "Run Task"
```

---

## 💡 Pro Tips

### 1. Keep Context
Keep Kiro running and reference previous answers:
```
> "Generate a user model"
> [Kiro generates it]
> "Now add authentication to it"
> [Kiro modifies based on context]
```

### 2. Iterate Quickly
Ask for improvements without repeating code:
```
> "Make this function faster"
> "Add error handling"
> "Make it support async"
```

### 3. Learn While Building
Ask for explanations while building:
```
> "Why did you use that approach?"
> "Can you explain this line?"
> "What are alternatives?"
```

### 4. Code Review
Paste code and ask for review:
```
> "Review this for security issues: [code]"
> "Suggest optimizations: [code]"
> "Any bugs here? [code]"
```

### 5. Use MCP Tools
Connect to external tools:
```
python cli.py mcp-add github "npx @modelcontextprotocol/server-github"
python cli.py mcp-connect github

# Now Kiro can help with GitHub operations!
```

---

## ⚠️ Important Don'ts

❌ Don't copy code without understanding it
❌ Don't skip testing generated code
❌ Don't use generated code in production without review
❌ Don't ignore security warnings from Kiro
❌ Don't close the chat if you need to keep working

✅ Do understand what code does before using
✅ Do test thoroughly before deploying
✅ Do customize generated code for your needs
✅ Do follow Kiro's security recommendations
✅ Do keep Kiro running during development

---

## 📊 Time Savings

| Task | Normal | With Kiro |
|------|--------|-----------|
| Generate boilerplate | 1 hour | 2 minutes ⚡ |
| Debug error | 1 hour | 5 minutes ⚡ |
| Learn framework | 2 hours | 15 minutes ⚡ |
| Code review | 30 min | 5 minutes ⚡ |
| Design API | 1 hour | 10 minutes ⚡ |
| **Total per day** | **5-8 hours** | **1-2 hours** ⚡ |

---

## 🎓 Learning Path

**Day 1:** Learn to use Kiro
```
python cli.py setup
python cli.py chat
Ask: "What can you help me with?"
Ask: "Generate a simple function"
```

**Day 2:** Build something small
```
python cli.py chat
Ask: "Generate a todo app backend"
Ask: "Generate a todo app frontend"
Ask: "How do I connect them?"
```

**Day 3:** Build something bigger
```
Build a full app using Kiro for all code generation,
debugging, and questions.
```

**Day 4+:** Integrate into workflow
```
Use Kiro for all development:
- Code generation
- Debugging
- Code review
- Learning
- Architecture decisions
```

---

## 🆘 Help & Support

### If Kiro isn't responding:
```bash
# Check if Ollama is running
ollama serve

# In another terminal, pull a model
ollama pull mistral

# Then try again
python cli.py setup
```

### If you need different model:
```bash
# See available models
ollama list

# Pull a different one
ollama pull neural-chat  # or llama2, dolphin-mixtral, etc

# Set in .env
LLMMODEL_NAME=neural-chat
```

### For more help:
```
- Read: USAGE_GUIDE.md
- Read: VS_CODE_GUIDE.md
- Read: README.md
- Run: python cli.py --help
```

---

## 🎯 Summary

**Start Here:**
```bash
python cli.py chat
```

**Keep It Running:**
- Don't close the chat
- Ask follow-up questions
- Build your entire app in the conversation

**Copy & Integrate:**
- Copy generated code into your project
- Test it
- Ask Kiro for improvements
- Keep building!

**That's literally it!** 🎉

---

**Made with ❤️ by Kiro AI Agent Team**
