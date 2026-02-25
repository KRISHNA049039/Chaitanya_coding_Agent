"""
Web UI for Kiro Agent
Simple Flask-based chat interface with approval workflow and database integration
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import uuid
import os
from agent import Agent
from config import load_config
from file_operations import approval_handler
from database import db_manager, init_database
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Store agents per session
agents = {}
pending_approvals = {}


def get_agent(session_id):
    """Get or create agent for session"""
    if session_id not in agents:
        config = load_config()
        agent = Agent(config=config)
        
        # IMPORTANT: Setup approval callback BEFORE any operations
        # This must be done after agent creation but before any tool usage
        def approval_callback(change_id, change):
            if session_id not in pending_approvals:
                pending_approvals[session_id] = {}
            pending_approvals[session_id][change_id] = {
                'change_id': change_id,
                'operation': change.operation,
                'path': change.path,
                'content': change.content,
                'old_content': change.old_content,
                'reason': change.reason,
                'diff': change.get_diff() if change.operation == 'modify' else None
            }
            print(f"[DEBUG] ✓ Approval callback triggered: {change_id} for {change.path}")
        
        # Set the callback on the agent's approval handler
        agent.approval_handler.set_approval_callback(approval_callback)
        print(f"[DEBUG] ✓ Approval callback registered for session {session_id}")
        
        agents[session_id] = agent
    
    return agents[session_id]


@app.route('/')
def index():
    """Serve the chat UI"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    message = data.get('message', '')
    session_id = session.get('session_id')
    
    print(f"\n[DEBUG] Received message: {message}")
    print(f"[DEBUG] Session ID: {session_id}")
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        agent = get_agent(session_id)
        print(f"[DEBUG] Agent created, starting run...")
        
        # For simple messages, use simple_chat instead of agentic loop
        simple_keywords = ['hello', 'hi', 'hey', 'thanks', 'thank you', 'bye', 'what is', 'explain', 'tell me about']
        is_simple = any(keyword in message.lower() for keyword in simple_keywords) and len(message.split()) < 15
        
        # Check if user wants to create/build/make something
        action_keywords = ['create', 'build', 'make', 'write', 'generate', 'add']
        needs_action = any(keyword in message.lower() for keyword in action_keywords)
        
        if is_simple and not needs_action:
            print(f"[DEBUG] Using simple chat mode")
            # Maintain conversation history in simple mode too
            from llm_client import Message
            agent.conversation_history.append(Message(role="user", content=message))
            
            # Trim history if too long (keep last 10 messages)
            if len(agent.conversation_history) > 10:
                agent.conversation_history = agent.conversation_history[-10:]
                print(f"[DEBUG] Trimmed conversation history to last 10 messages")
            
            response = agent.llm.chat(
                messages=agent.conversation_history,
                temperature=agent.config.llm_config.temperature,
                max_tokens=agent.config.llm_config.max_tokens,
                system_prompt=agent.config.llm_config.system_prompt,
            )
            agent.conversation_history.append(Message(role="assistant", content=response))
        else:
            print(f"[DEBUG] Using agentic mode with max 3 iterations")
            
            # Trim history if too long (keep last 6 messages for agentic mode)
            if len(agent.conversation_history) > 6:
                agent.conversation_history = agent.conversation_history[-6:]
                print(f"[DEBUG] Trimmed conversation history to last 6 messages")
            
            # Agentic mode maintains history automatically
            response = agent.run(message, max_iterations=3, verbose=True)
        
        print(f"[DEBUG] Agent finished, response length: {len(response)}")
        print(f"[DEBUG] Conversation history: {len(agent.conversation_history)} messages")
        
        # Check for pending approvals
        print(f"[DEBUG] Checking pending_approvals dict: {list(pending_approvals.keys())}")
        approvals = pending_approvals.get(session_id, {})
        print(f"[DEBUG] Approvals for session {session_id}: {list(approvals.keys())}")
        print(f"[DEBUG] Pending approvals count: {len(approvals)}")
        
        # Convert approvals to list
        approval_list = []
        for change_id, approval_data in approvals.items():
            print(f"[DEBUG] Approval {change_id}: {approval_data.get('operation')} {approval_data.get('path')}")
            approval_list.append(approval_data)
        
        print(f"[DEBUG] Returning {len(approval_list)} approvals to browser")
        
        return jsonify({
            'response': response,
            'pending_approvals': approval_list
        })
    
    except TimeoutError:
        print("[DEBUG] Timeout error")
        return jsonify({'error': 'Request timed out. Please try again with a simpler prompt.'}), 408
    except ConnectionError:
        print("[DEBUG] Connection error")
        return jsonify({'error': 'Cannot connect to Ollama. Make sure it is running: ollama serve'}), 503
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[DEBUG] Error in chat: {error_details}")
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/api/approve', methods=['POST'])
def approve():
    """Handle approval/rejection of file operations"""
    data = request.json
    change_id = data.get('change_id')
    approved = data.get('approved', False)
    session_id = session.get('session_id')
    
    print(f"\n[DEBUG] Approval request: change_id={change_id}, approved={approved}")
    
    if not change_id:
        return jsonify({'error': 'No change_id provided'}), 400
    
    try:
        agent = get_agent(session_id)
        
        print(f"[DEBUG] Agent retrieved, processing approval...")
        
        if approved:
            result = agent.approval_handler.approve_change(change_id)
            print(f"[DEBUG] Approval result: success={result.success}, output={result.output}")
        else:
            result = agent.approval_handler.reject_change(change_id)
            print(f"[DEBUG] Rejection result: success={result.success}, output={result.output}")
        
        # Remove from pending
        if session_id in pending_approvals and change_id in pending_approvals[session_id]:
            del pending_approvals[session_id][change_id]
            print(f"[DEBUG] Removed from pending approvals")
        
        return jsonify({
            'success': result.success,
            'message': result.output if result.success else result.error
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[DEBUG] Error in approve: {error_details}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get agent status"""
    session_id = session.get('session_id')
    
    try:
        agent = get_agent(session_id)
        return jsonify(agent.get_status())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear():
    """Clear conversation history"""
    session_id = session.get('session_id')
    
    if session_id in agents:
        agents[session_id].conversation_history = []
    
    if session_id in pending_approvals:
        pending_approvals[session_id] = {}
    
    return jsonify({'success': True})


if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("\n" + "="*60)
    print("🚀 Kiro Agent Web UI Starting...")
    print("="*60)
    print("\n📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 Features:")
    print("   - Chat with your agent")
    print("   - Approve/reject file operations")
    print("   - Execute shell commands")
    print("   - Search the web")
    print("   - Persistent conversation history")
    print("\n⚠️  Make sure Ollama is running: ollama serve")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
