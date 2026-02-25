# 🎯 Integrate Your Agent into Kiro IDE

Make your agent available in Kiro IDE's chat interface!

## Option 1: Use Your Agent in Kiro IDE Chat

### Step 1: Start Your Agent Server

```cmd
cd Chaitanya_coding_Agent
python web_ui.py
```

Keep this running on http://localhost:5000

### Step 2: Create MCP Server Wrapper

Your agent needs to be exposed as an MCP server for Kiro IDE to use it.

Create `mcp_server_wrapper.py`:

```python
"""
MCP Server wrapper for Kiro Agent
Exposes your agent as an MCP server that Kiro IDE can connect to
"""
import asyncio
import json
import sys
from typing import Any, Dict
import requests

class KiroAgentMCPServer:
    """MCP Server that wraps your Kiro Agent"""
    
    def __init__(self, agent_url: str = "http://localhost:5000"):
        self.agent_url = agent_url
        self.session_id = "kiro-ide-session"
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "chat_with_agent",
                        "description": "Chat with your Kiro Agent",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "Message to send to agent"
                                }
                            },
                            "required": ["message"]
                        }
                    }
                ]
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "chat_with_agent":
                message = arguments.get("message")
                
                # Call your agent
                response = requests.post(
                    f"{self.agent_url}/api/chat",
                    json={
                        "message": message,
                        "session_id": self.session_id,
                        "stream": False
                    }
                )
                
                result = response.json()
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": result.get("response", "")
                        }
                    ]
                }
        
        return {"error": "Unknown method"}
    
    async def run(self):
        """Run MCP server on stdio"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                request = json.loads(line)
                response = await self.handle_request(request)
                
                print(json.dumps(response), flush=True)
                
            except Exception as e:
                error_response = {"error": str(e)}
                print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    server = KiroAgentMCPServer()
    asyncio.run(server.run())
```

### Step 3: Configure Kiro IDE

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "my-kiro-agent": {
      "command": "python",
      "args": ["C:/path/to/Chaitanya_coding_Agent/mcp_server_wrapper.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Step 4: Restart Kiro IDE

Your agent will now be available as an MCP tool in Kiro IDE!

---

## Option 2: Direct Chat (Simpler)

Just use the CLI or Web UI alongside Kiro IDE:

### Terminal in Kiro IDE:

```cmd
# Start CLI chat
python cli_chat.py
```

Or open browser:
```cmd
python web_ui.py
# Open http://localhost:5000
```

---

## Option 3: Use VS Code Extension

If you're using VS Code (not Kiro IDE):

1. Install the extension we built
2. Start the server
3. Chat in the sidebar

---

## Recommended: Use CLI in Kiro IDE Terminal

The easiest way:

1. Open terminal in Kiro IDE (bottom panel)
2. Run:
   ```cmd
   cd Chaitanya_coding_Agent
   python cli_chat.py
   ```
3. Chat with streaming responses!

This gives you:
- ✅ Streaming responses
- ✅ Inline approvals
- ✅ Side-by-side with code
- ✅ No extra setup needed

---

**Quick Start:**
```cmd
python cli_chat.py
```

That's the fastest way to use your agent in Kiro IDE!
