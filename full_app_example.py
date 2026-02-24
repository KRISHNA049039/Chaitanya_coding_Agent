#!/usr/bin/env python3
"""
Complete Todo App Building Example with Kiro

This is a real, step-by-step example showing how to use Kiro to build a complete application.
You can follow this exactly to see the whole workflow.
"""

from agent import Agent
import asyncio

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         BUILDING A TODO APP WITH KIRO - LIVE DEMO             ║
║                                                               ║
║  This example shows how to use Kiro as your development      ║
║  assistant to build a complete application.                   ║
║                                                               ║
║  You'll see:                                                  ║
║  1. Backend code generation                                   ║
║  2. Frontend code generation                                  ║
║  3. Connection between frontend and backend                   ║
║  4. Database schema design                                    ║
║  5. Error handling and improvements                           ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    agent = Agent()
    
    input("Press Enter to start the demo...")
    
    # Phase 1: Architecture
    print("\n" + "="*70)
    print("PHASE 1: PLANNING & ARCHITECTURE")
    print("="*70)
    
    print("\n📝 First, let's plan our app architecture...\n")
    
    arch_prompt = """I want to build a Todo App with these requirements:
    - Users can create, read, update, delete todos
    - Each todo has: title, description, due date, completed status
    - Users can mark todos as complete
    - Users can filter todos by status
    - Simple authentication (username/password)
    
    What's the best tech stack and architecture for this?"""
    
    print(f"👤 You: {arch_prompt[:80]}...\n")
    print("🤖 Kiro thinking...\n")
    
    architecture = agent.simple_chat(arch_prompt)
    print(f"🤖 Kiro:\n{architecture}\n")
    
    input("Press Enter to continue to backend generation...")
    
    # Phase 2: Backend
    print("\n" + "="*70)
    print("PHASE 2: BACKEND CODE GENERATION")
    print("="*70)
    
    print("\n💻 Now let's generate the backend code...\n")
    
    backend_prompt = """Generate a FastAPI backend for the Todo app. Include:
    
    1. Database models (User, Todo) using SQLAlchemy
    2. Pydantic schemas for validation
    3. Authentication endpoint (login)
    4. CRUD endpoints:
       - GET /todos (get all user's todos)
       - POST /todos (create new todo)
       - PUT /todos/{id} (update todo)
       - DELETE /todos/{id} (delete todo)
    5. Filtering endpoint:
       - GET /todos?status=completed|pending|all
    6. Main FastAPI app setup
    
    Use SQLite for simplicity. Make it production-ready."""
    
    print(f"👤 You: Generate FastAPI backend...\n")
    print("🤖 Kiro generating code...\n")
    
    backend_code = agent.run(backend_prompt, max_iterations=3)
    
    # Save the generated code
    with open("GENERATED_BACKEND.py", "w") as f:
        f.write(backend_code)
    
    print(f"✅ Backend generated and saved to GENERATED_BACKEND.py")
    print(f"\nBackend preview (first 800 chars):\n")
    print(backend_code[:800])
    print("...[code continues]...")
    
    input("\nPress Enter to continue to frontend...")
    
    # Phase 3: Frontend
    print("\n" + "="*70)
    print("PHASE 3: FRONTEND CODE GENERATION")
    print("="*70)
    
    print("\n🎨 Now let's generate the React frontend...\n")
    
    frontend_prompt = """Generate a React component for the Todo App with:
    
    1. Login/Register form with email and password
    2. Todo list display showing all todos
    3. Add new todo form with title, description, due date
    4. Each todo showing:
       - Title and description
       - Due date
       - Complete/incomplete checkbox
       - Delete button
    5. Filter buttons: All, Completed, Pending
    6. Responsive design using Tailwind CSS
    
    Include proper state management and make it interactive.
    Assume the backend is at http://localhost:8000"""
    
    print(f"👤 You: Generate React frontend...\n")
    print("🤖 Kiro generating code...\n")
    
    frontend_code = agent.run(frontend_prompt, max_iterations=3)
    
    # Save the generated code
    with open("GENERATED_FRONTEND.jsx", "w") as f:
        f.write(frontend_code)
    
    print(f"✅ Frontend generated and saved to GENERATED_FRONTEND.jsx")
    print(f"\nFrontend preview (first 800 chars):\n")
    print(frontend_code[:800])
    print("...[code continues]...")
    
    input("\nPress Enter to continue to API integration...")
    
    # Phase 4: Integration
    print("\n" + "="*70)
    print("PHASE 4: API INTEGRATION")
    print("="*70)
    
    print("\n🔌 Let's connect frontend to backend...\n")
    
    integration_prompt = """I have this React component for todos and a FastAPI backend 
    at http://localhost:8000.
    
    The backend has these endpoints:
    - POST /login (returns token)
    - GET /todos (returns user's todos, needs Authorization header)
    - POST /todos (creates todo, needs Authorization header)
    - PUT /todos/{id} (updates todo)
    - DELETE /todos/{id} (deletes todo)
    
    Show me how to:
    1. Handle authentication and store the token
    2. Make API calls with proper headers
    3. Handle loading and error states
    4. Include proper error handling"""
    
    print(f"👤 You: How do I integrate the API?\n")
    print("🤖 Kiro generating integration code...\n")
    
    integration = agent.simple_chat(integration_prompt)
    
    print(f"🤖 Kiro:\n{integration}\n")
    
    input("\nPress Enter to continue to deployment...")
    
    # Phase 5: Deployment
    print("\n" + "="*70)
    print("PHASE 5: DEPLOYMENT GUIDE")
    print("="*70)
    
    print("\n🚀 Let's prepare for deployment...\n")
    
    deploy_prompt = """Now I want to deploy this Todo app. Give me step-by-step instructions for:
    
    1. Deploy FastAPI backend to production (Heroku, Railway, or AWS)
    2. Deploy React frontend to production (Vercel, Netlify, or AWS)
    3. Setup environment variables
    4. Database migration for production
    5. Basic security checklist
    
    Make it as simple as possible."""
    
    print(f"👤 You: How do I deploy this app?\n")
    print("🤖 Kiro creating deployment guide...\n")
    
    deployment = agent.simple_chat(deploy_prompt)
    
    print(f"🤖 Kiro:\n{deployment}\n")
    
    # Summary
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    
    print("""
    You've just seen how to use Kiro to:
    
    1. ✅ Plan your app architecture
    2. ✅ Generate backend code (FastAPI)
    3. ✅ Generate frontend code (React)  
    4. ✅ Integrate frontend and backend
    5. ✅ Create deployment guide
    
    GENERATED FILES:
    - GENERATED_BACKEND.py - Ready to use FastAPI app
    - GENERATED_FRONTEND.jsx - Ready to use React component
    
    NEXT STEPS:
    1. Review the generated code
    2. Customize as needed for your use case
    3. Test the code locally
    4. Deploy to production
    
    TIPS:
    - Keep Kiro running while developing: python cli.py chat
    - Ask Kiro for help with bugs or features
    - Use Kiro to review your code before submitting
    - Ask Kiro for explanations when stuck
    
    WORKFLOW:
    Terminal 1: python cli.py chat (keep running)
    Terminal 2: Your build/dev commands
    Terminal 3: Testing/deployment
    
    That's it! You now know how to use Kiro to build apps! 🎉
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Ollama running: ollama serve")
        print("2. A model pulled: ollama pull mistral")
        print("3. Dependencies installed: pip install -r requirements.txt")
