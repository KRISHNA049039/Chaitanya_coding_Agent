# Using Kiro to Build Your Apps

This guide shows how to integrate Kiro into your development workflow and build applications with AI assistance.

## 🚀 Usage Patterns

### Pattern 1: One-Time Setup → Keep Running (Recommended)

**Start Kiro Once, Keep Using It:**

```bash
# Terminal 1: Start Kiro (keep running)
python cli.py chat

# Terminal 2: Work on your app
# Ask Kiro questions while developing
# Kiro stays running in background
```

**Benefits:**
- ✅ No restart needed
- ✅ Context preserved across questions
- ✅ Quick interactive development
- ✅ Ask follow-up questions

### Pattern 2: Run Kiro Only When Needed

```bash
# When you need code generation
python cli.py code "write a function to handle authentication"

# When you need to debug
python cli.py chat "why is this code throwing an error?"

# When you need explanation
python cli.py chat "explain how async/await works"
```

**Benefits:**
- ✅ Minimal resource usage
- ✅ Single purpose runs
- ✅ Quick answers

### Pattern 3: Integrate Kiro into Your Build Process

Create a build helper script:

```python
# build_helper.py
from agent import Agent
import sys

def get_help(task: str) -> str:
    """Get Kiro's help for a development task"""
    agent = Agent()
    return agent.run(task, verbose=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        response = get_help(task)
        print(response)
    else:
        print("Usage: python build_helper.py 'your task here'")
```

Then use in your workflow:
```bash
# Get help while building
python build_helper.py "fix this TypeScript error"
python build_helper.py "optimize this database query"
python build_helper.py "add error handling to this function"
```

## 💡 Real-World Development Workflows

### Workflow 1: Web App Development

```
┌─ Start Kiro (Terminal 1): python cli.py chat
│
├─ Development (Terminal 2):
│  ├─ Start dev server: npm start
│  ├─ Ask Kiro: "Create a React component for user auth"
│  ├─ Kiro generates code
│  ├─ Copy code into your app
│  ├─ Ask Kiro: "Debug why useState isn't updating"
│  ├─ Kiro fixes it
│  └─ Continue...
│
└─ Keep Kiro running until done
```

**Example Session:**
```bash
# Terminal 1
python cli.py chat

# You (in chat)
> "Create a React component for a login form with validation"

# Kiro returns:
import React, { useState } from 'react';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  // ... full component code

# Copy the code into your React app

> "Add error handling for failed login attempts"

# Kiro updates the component with error handling
```

### Workflow 2: Backend API Development

```
┌─ Start Kiro
│
├─ Development:
│  ├─ Ask: "Create a FastAPI endpoint for user registration"
│  ├─ Kiro generates endpoint
│  ├─ Ask: "Add JWT authentication"
│  ├─ Ask: "Create database models for PostgreSQL"
│  ├─ Ask: "Generate migration script"
│  └─ Continue building...
│
└─ Keep Kiro running
```

### Workflow 3: Data Processing

```
┌─ Start Kiro
│
├─ Development:
│  ├─ Ask: "Create a script to process CSV files"
│  ├─ Kiro generates script
│  ├─ Ask: "Add parallel processing for performance"
│  ├─ Ask: "How to handle missing values in data?"
│  └─ Continue...
│
└─ Keep Kiro running
```

## 🔧 Integration with Popular Frameworks

### With Next.js

```bash
# Terminal 1: Start Kiro
python cli.py chat

# Terminal 2: Start Next.js
npm run dev

# Ask Kiro for help:
# "Create a Next.js page with API routes for a todo app"
# "Add authentication with NextAuth"
# "Optimize images with Next.js Image component"
```

### With Django

```bash
# Terminal 1: Start Kiro
python cli.py chat

# Terminal 2: Django development
python manage.py runserver

# Ask Kiro:
# "Create a Django model for blog posts with relations"
# "Generate views and URLs for CRUD operations"
# "Add pagination to list view"
```

### With Python Flask

```bash
# Terminal 1: Start Kiro
python cli.py chat

# Terminal 2: Flask development
flask run

# Ask Kiro:
# "Create Flask routes for user management"
# "Add database migrations"
# "Implement caching"
```

## 🛠️ Using Kiro for Code Review & Debugging

### Get Code Reviewed

```bash
# Open a file in your app
# Copy problematic code
# Paste into Kiro chat:

You: "Review this code for bugs and performance issues:
```python
def process_data(items):
    result = []
    for i in range(len(items)):
        if items[i] > 0:
            result.append(items[i] * 2)
    return result
```
"

Kiro: "This has O(n) complexity which is good. Suggestions:
1. Use list comprehension for clarity
2. Add type hints
3. Add docstring"
```

### Debug Issues

```bash
You: "My React component keeps re-rendering. Here's the code:
```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    fetchUsers();
  }, []);
  
  const fetchUsers = async () => {
    const data = await api.getUsers();
    setUsers(data);
  };
  
  return ...
}
```

Why is this rendering so many times?"

Kiro: "The issue is that `fetchUsers` is not memoized. Move it outside 
useEffect or use useCallback. Here's the fix..."
```

## 📱 Build Your Own Apps Using Kiro as Backend

You can embed Kiro in your own applications:

### Simple Python App

```python
# my_app.py
from agent import Agent
import asyncio
from config import MCPServerConfig

class AppBuilder:
    def __init__(self):
        self.agent = Agent()
    
    def generate_code(self, requirement: str) -> str:
        """Use Kiro to generate code"""
        return self.agent.run(requirement)
    
    def debug_code(self, code: str, error: str) -> str:
        """Use Kiro to debug"""
        prompt = f"Debug this code:\n{code}\n\nError: {error}"
        return self.agent.simple_chat(prompt)
    
    def get_suggestion(self, code: str) -> str:
        """Get improvement suggestions"""
        return self.agent.simple_chat(f"Review and suggest improvements:\n{code}")

# Usage
app = AppBuilder()

# Generate code
code = app.generate_code("Create a function to validate email addresses")
print(code)

# Get debugging help
error = app.debug_code(code, "ValueError: invalid email format")
print(error)

# Get suggestions
suggestions = app.get_suggestion(code)
print(suggestions)
```

### Web App with Kiro Backend

```python
# app.py (Flask Example)
from flask import Flask, request, jsonify
from agent import Agent
import asyncio

app = Flask(__name__)
agent = Agent()

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate code using Kiro"""
    data = request.json
    requirement = data.get('requirement')
    
    code = agent.run(requirement)
    return jsonify({'code': code})

@app.route('/api/debug', methods=['POST'])
def debug():
    """Debug code using Kiro"""
    data = request.json
    code = data.get('code')
    error = data.get('error')
    
    prompt = f"Debug this:\n{code}\n\nError: {error}"
    solution = agent.simple_chat(prompt)
    return jsonify({'solution': solution})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with Kiro"""
    data = request.json
    message = data.get('message')
    
    response = agent.simple_chat(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
```

## 🎯 Step-by-Step: Building a Real App with Kiro

### Example: Building a Todo App

**Step 1: Start Kiro**
```bash
python cli.py chat
```

**Step 2: Generate Backend**
```
You: "Create a FastAPI backend for a todo app with:
- User authentication
- CRUD operations for todos
- SQLAlchemy models
- Pydantic schemas"

# Kiro generates complete backend code
# Copy into your project
```

**Step 3: Generate Frontend**
```
You: "Create a React component for a todo app with:
- List of todos
- Add new todo form
- Edit/delete buttons
- Filter by completed status"

# Kiro generates React component
# Copy into your frontend
```

**Step 4: Connect Backend & Frontend**
```
You: "How do I connect this React component to my FastAPI backend?"

# Kiro shows you the API calls needed
# Add them to your component
```

**Step 5: Add Features**
```
You: "Add drag-and-drop functionality to reorder todos"
You: "Add due dates to todos"
You: "Add categories for organizing todos"

# Keep building with Kiro's help
```

## 📊 Comparison: With vs Without Kiro

| Task | Without Kiro | With Kiro |
|------|--------------|----------|
| Generate code | Search StackOverflow, 30min | Ask Kiro, 2min ✅ |
| Debug error | Try fixes, 1hour | Ask Kiro, 5min ✅ |
| Learn framework | Read docs, 2hours | Ask Kiro, 15min ✅ |
| Code review | Read own code, miss issues | Kiro reviews, catches bugs ✅ |
| Add feature | Write from scratch, 2hours | Kiro generates, 10min ✅ |

## 🎓 Best Practices

### Do ✅
- Use Kiro for code generation and suggestions
- Ask for explanations when stuck
- Ask Kiro to review your code
- Use for debugging and error fixes
- Keep it running during development
- Use MCP tools to extend capabilities
- Version control generated code

### Don't ❌
- Copy code without understanding it
- Use generated code without testing
- Rely only on Kiro without learning
- Ignore security recommendations
- Not customize generated code for your needs
- Skip testing generated code

## 🔄 Workflow Best Practices

### Development Session Template

```bash
# 1. Start with Kiro
python cli.py chat

# 2. Initial code generation
# Ask for main components/endpoints

# 3. Interactive refinement
# Ask for tweaks, improvements, debugging

# 4. Real-world testing
# Test generated code in your app

# 5. Ask for improvements
# "Make this more efficient", "Add error handling", etc.

# 6. Keep Kiro running
# Don't close until development is done
```

### Terminal Setup (Recommended)

```bash
# Terminal Window 1: Kiro (stays running)
python cli.py chat

# Terminal Window 2: Your app
npm start        # or python app.py, or ruby rails s, etc.

# Terminal Window 3: Testing/builds
npm test         # or your build/test commands

# Terminal Window 4: Additional work
# git, file operations, etc.
```

## 🚀 Quick Reference

### Start Kiro Once
```bash
python cli.py chat
```

Then in the same chat session, ask for:
- Code generation
- Debugging help
- Explanations
- Code review
- Optimization suggestions
- Feature additions

### One-Off Tasks
```bash
# Generate specific code
python cli.py code "write a fibonacci function"

# Get quick answer
python cli.py chat "how does promise.all work?"
```

### Integrate into Your Build
```python
# build_helper.py
from agent import Agent

def help_with_task(task):
    agent = Agent()
    return agent.run(task)

# Then use everywhere in your workflow
```

## 📚 Common Use Cases

| Scenario | Command/Approach |
|----------|-----------------|
| "I'm stuck on this bug" | `python cli.py chat` → describe the bug |
| "Generate boilerplate code" | `python cli.py code "generate..."` |
| "Learn how to use X" | `python cli.py chat "explain X"` |
| "Review my code" | Copy code into chat, ask for review |
| "Optimize this function" | Paste code, ask: "optimize this" |
| "Add feature X" | Ask in chat session |
| "Database schema help" | `python cli.py chat`, describe schema |

---

**TL;DR:** 
- Start Kiro once with `python cli.py chat`
- Keep it running during development
- Ask it anything while building
- Copy generated code into your app
- Continue building with its help
- No need to restart!
