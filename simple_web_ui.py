"""
Simplified Web UI with better debugging
"""
from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS
import uuid
import secrets
import sys
import traceback

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kiro Agent - Simple UI</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        #chat { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .agent { background: #f5f5f5; }
        .error { background: #ffebee; color: #c62828; }
        #input { width: 70%; padding: 10px; }
        button { padding: 10px 20px; }
        .thinking { color: #666; font-style: italic; }
    </style>
</head>
<body>
    <h1>🤖 Kiro Agent - Debug Mode</h1>
    <div id="chat"></div>
    <input type="text" id="input" placeholder="Type message..." onkeypress="if(event.key==='Enter') send()">
    <button onclick="send()">Send</button>
    <button onclick="stop()" id="stopBtn" style="display:none; background:#f44336; color:white;">Stop</button>
    
    <script>
        let processing = false;
        let controller = null;
        
        function addMsg(text, type) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
        
        function showThinking() {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.id = 'thinking';
            div.className = 'message thinking';
            div.textContent = '🤔 Agent thinking...';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
        
        function hideThinking() {
            const el = document.getElementById('thinking');
            if (el) el.remove();
        }
        
        async function send() {
            if (processing) return;
            
            const input = document.getElementById('input');
            const msg = input.value.trim();
            if (!msg) return;
            
            processing = true;
            document.getElementById('stopBtn').style.display = 'inline';
            addMsg(msg, 'user');
            input.value = '';
            showThinking();
            
            controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 30000); // 30 sec timeout
            
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg}),
                    signal: controller.signal
                });
                
                clearTimeout(timeout);
                const data = await res.json();
                hideThinking();
                
                if (data.error) {
                    addMsg('ERROR: ' + data.error, 'error');
                } else {
                    addMsg(data.response, 'agent');
                }
            } catch (err) {
                clearTimeout(timeout);
                hideThinking();
                if (err.name === 'AbortError') {
                    addMsg('⏱️ Timeout! Agent took too long.', 'error');
                } else {
                    addMsg('❌ Error: ' + err.message, 'error');
                }
            } finally {
                processing = false;
                controller = null;
                document.getElementById('stopBtn').style.display = 'none';
            }
        }
        
        function stop() {
            if (controller) {
                controller.abort();
                hideThinking();
                addMsg('⏹️ Stopped', 'error');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    if 'id' not in session:
        session['id'] = str(uuid.uuid4())
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        print(f"\n{'='*60}")
        print(f"Received: {message}")
        print(f"{'='*60}")
        
        # Import here to see errors
        from agent import Agent
        from config import load_config
        
        print("Creating agent...")
        config = load_config()
        agent = Agent(config=config)
        
        print("Running agent...")
        sys.stdout.flush()
        
        # Run with max 3 iterations and timeout
        response = agent.run(message, max_iterations=3, verbose=True)
        
        print(f"\nResponse: {response[:100]}...")
        print(f"{'='*60}\n")
        sys.stdout.flush()
        
        return jsonify({'response': response})
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"\n❌ ERROR: {error_msg}")
        traceback.print_exc()
        sys.stdout.flush()
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Simple Kiro Agent UI")
    print("="*60)
    print("\n📱 Open: http://localhost:5001")
    print("⚠️  Watch this terminal for debug output")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
