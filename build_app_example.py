#!/usr/bin/env python3
"""
Practical Example: Build a Todo App with Kiro

This shows a complete workflow of using Kiro to build a real application.
You can follow this step-by-step to understand how to use Kiro in your projects.
"""

from agent import Agent
import json

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}\n")

def demo_code_generation():
    """Example 1: Generate backend code"""
    print_section("Step 1: Backend Code Generation")
    
    agent = Agent()
    
    prompt = """Generate a Python FastAPI application with these features:
1. User authentication (simple token-based)
2. Todo CRUD operations
3. SQLite database
4. Include models, schemas, and main app file

Start with just the main app.py file."""
    
    print(f"Request: {prompt}\n")
    print("Generating backend...")
    
    code = agent.run(prompt, verbose=False)
    
    # Save generated code
    with open("generated_backend.py", "w") as f:
        f.write(code)
    
    print(f"\n✅ Backend generated! (saved to generated_backend.py)")
    print(f"\nPreview (first 500 chars):\n{code[:500]}...")
    
    return code

def demo_frontend_generation():
    """Example 2: Generate frontend code"""
    print_section("Step 2: Frontend Code Generation")
    
    agent = Agent()
    
    prompt = """Generate a React component for a todos list with:
1. Display list of todos
2. Add new todo form
3. Mark todo as complete/incomplete
4. Delete todo
5. Filter (show all, completed, pending)

Make it look nice with Tailwind CSS."""
    
    print(f"Request: {prompt}\n")
    print("Generating frontend...")
    
    code = agent.run(prompt, verbose=False)
    
    # Save generated code
    with open("generated_todos.jsx", "w") as f:
        f.write(code)
    
    print(f"\n✅ Frontend generated! (saved to generated_todos.jsx)")
    print(f"\nPreview (first 500 chars):\n{code[:500]}...")
    
    return code

def demo_code_review():
    """Example 3: Get code review"""
    print_section("Step 3: Code Review & Improvements")
    
    agent = Agent()
    
    # Some sample code to review
    sample_code = """
def get_todos(user_id):
    todos = []
    with open(f"todos_{user_id}.txt", "r") as f:
        for line in f:
            todos.append(line.strip())
    return todos
"""
    
    prompt = f"""Review this code and suggest improvements:

{sample_code}

Focus on:
- Security issues
- Performance
- Best practices
- Error handling"""
    
    print(f"Reviewing code...\n")
    review = agent.simple_chat(prompt)
    
    print(f"Code Review:\n{review}")
    
    # Save review
    with open("code_review.txt", "w") as f:
        f.write(review)
    
    print(f"\n✅ Review saved to code_review.txt")

def demo_debugging():
    """Example 4: Debug common issues"""
    print_section("Step 4: Debugging Help")
    
    agent = Agent()
    
    buggy_code = """
const axios = require('axios');

async function fetchTodos() {
    const response = await axios.get('/api/todos');
    setTodos(response.data);  // Error: setTodos is not defined
    return response.data;
}
"""
    
    prompt = f"""My React code is throwing an error. Fix it:

{buggy_code}

Error message: "TypeError: setTodos is not a function"
"""
    
    print("Debugging your code...")
    fix = agent.simple_chat(prompt)
    
    print(f"Fix:\n{fix}")
    
    with open("debugging_fix.txt", "w") as f:
        f.write(fix)
    
    print(f"\n✅ Fix saved to debugging_fix.txt")

def demo_api_integration():
    """Example 5: Get API integration help"""
    print_section("Step 5: API Integration Guide")
    
    agent = Agent()
    
    prompt = """I have a FastAPI backend at http://localhost:8000 with these endpoints:
- GET /api/todos
- POST /api/todos
- PUT /api/todos/{id}
- DELETE /api/todos/{id}

Show me how to call these from a React component using fetch or axios.
Include error handling and loading states."""
    
    print("Generating integration code...")
    
    integration = agent.simple_chat(prompt)
    
    with open("api_integration.js", "w") as f:
        f.write(integration)
    
    print(f"API Integration:\n{integration[:500]}...\n")
    print(f"✅ Integration code saved to api_integration.js")

def demo_step_by_step_development():
    """Example 6: Step-by-step development assistance"""
    print_section("Step 6: Interactive Development Walkthrough")
    
    agent = Agent()
    
    # Initialize conversation
    print("Starting interactive development session...\n")
    
    # Step 1
    print("[Step 1] Request initial architecture")
    step1_prompt = "I want to build a simple notes app. What should the architecture look like?"
    print(f"You: {step1_prompt}")
    
    response1 = agent.simple_chat(step1_prompt)
    print(f"\nKiro: {response1[:300]}...\n")
    
    # Step 2
    print("[Step 2] Get database schema")
    step2_prompt = "Good! Now create a SQLAlchemy model for notes with: id, title, content, created_at, updated_at"
    print(f"You: {step2_prompt}")
    
    response2 = agent.simple_chat(step2_prompt)
    print(f"\nKiro: {response2[:300]}...\n")
    
    # Step 3
    print("[Step 3] Add validation")
    step3_prompt = "Add Pydantic validation schemas for creating and updating notes"
    print(f"You: {step3_prompt}")
    
    response3 = agent.simple_chat(step3_prompt)
    print(f"\nKiro: {response3[:300]}...\n")
    
    print("✅ Development session complete!")

def demo_performance_optimization():
    """Example 7: Get optimization suggestions"""
    print_section("Step 7: Performance Optimization")
    
    agent = Agent()
    
    slow_function = """
def get_user_todos(user_id):
    todos = []
    for todo_id in range(1, 10000):
        todo = database.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
        if todo:
            todos.append(todo)
    return todos
"""
    
    prompt = f"""This function is slow. How can I optimize it?

{slow_function}

It's used to fetch a user's todos. The user might have 100-1000 todos."""
    
    print("Analyzing performance...")
    optimization = agent.simple_chat(prompt)
    
    with open("optimizations.txt", "w") as f:
        f.write(optimization)
    
    print(f"Optimization Tips:\n{optimization}")
    print(f"\n✅ Saved to optimizations.txt")

def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("🚀 KIRO APP BUILDING DEMONSTRATION")
    print("="*60)
    print("""
This guide shows 7 practical examples of using Kiro to build apps:

1. Backend Code Generation - Generate FastAPI boilerplate
2. Frontend Code Generation - Generate React components  
3. Code Review & Improvements - Get feedback on code
4. Debugging Help - Fix errors in your code
5. API Integration - Connect front & backend
6. Interactive Development - Step-by-step guidance
7. Performance Optimization - Improve code efficiency

Each example demonstrates a different use case you'll encounter
when building real applications.

Choose an example to run (1-7), or 'all' to run everything:
    """)
    
    choice = input("Enter your choice (1-7 or 'all'): ").strip().lower()
    
    examples = {
        '1': demo_code_generation,
        '2': demo_frontend_generation,
        '3': demo_code_review,
        '4': demo_debugging,
        '5': demo_api_integration,
        '6': demo_step_by_step_development,
        '7': demo_performance_optimization,
    }
    
    if choice == 'all':
        for example in examples.values():
            try:
                example()
            except Exception as e:
                print(f"Error: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
