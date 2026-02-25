"""
Kiro IDE Integration
Allows your agent to work directly within Kiro IDE with approval workflow
"""
import json
import sys
from typing import Optional, Dict, Any
from file_operations import FileChange, approval_handler
from agent import Agent
from config import load_config


class KiroIDEBridge:
    """Bridge for integrating with Kiro IDE"""
    
    def __init__(self):
        self.agent: Optional[Agent] = None
    
    def setup_agent(self) -> Agent:
        """Setup agent with Kiro IDE integration"""
        config = load_config()
        agent = Agent(config=config)
        
        # Setup approval callback
        def approval_callback(change_id: str, change: FileChange):
            self.send_approval_request(change_id, change)
        
        agent.approval_handler.set_approval_callback(approval_callback)
        self.agent = agent
        return agent
    
    def send_approval_request(self, change_id: str, change: FileChange) -> None:
        """Send approval request to Kiro IDE"""
        request = {
            "type": "file_operation_approval",
            "change_id": change_id,
            "operation": change.operation,
            "path": change.path,
            "reason": change.reason,
            "content": change.content,
            "old_content": change.old_content,
            "diff": change.get_diff() if change.operation == "modify" else None
        }
        
        # Output as JSON for Kiro IDE to parse
        print(f"\n__KIRO_APPROVAL_REQUEST__:{json.dumps(request)}", flush=True)
    
    def handle_approval_response(self, change_id: str, approved: bool) -> str:
        """Handle approval response from Kiro IDE"""
        if not self.agent:
            return "Error: Agent not initialized"
        
        if approved:
            result = self.agent.approval_handler.approve_change(change_id)
        else:
            result = self.agent.approval_handler.reject_change(change_id)
        
        if result.success:
            return result.output
        else:
            return f"Error: {result.error}"
    
    def chat(self, message: str, verbose: bool = False) -> str:
        """Process a chat message"""
        if not self.agent:
            self.setup_agent()
        
        return self.agent.run(message, verbose=verbose)


def run_kiro_ide_mode():
    """Run agent in Kiro IDE integration mode"""
    bridge = KiroIDEBridge()
    bridge.setup_agent()
    
    print("Kiro Agent ready in IDE mode. Type your message:", flush=True)
    
    try:
        while True:
            line = input().strip()
            
            if not line:
                continue
            
            # Check for approval responses
            if line.startswith("__KIRO_APPROVAL_RESPONSE__:"):
                try:
                    response_data = json.loads(line[len("__KIRO_APPROVAL_RESPONSE__:"):])
                    change_id = response_data.get("change_id")
                    approved = response_data.get("approved", False)
                    
                    result = bridge.handle_approval_response(change_id, approved)
                    print(f"\n{result}\n", flush=True)
                except Exception as e:
                    print(f"\nError handling approval: {e}\n", flush=True)
                continue
            
            # Check for exit commands
            if line.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!", flush=True)
                break
            
            # Process as chat message
            try:
                response = bridge.chat(line, verbose=False)
                print(f"\n{response}\n", flush=True)
            except Exception as e:
                print(f"\nError: {e}\n", flush=True)
    
    except KeyboardInterrupt:
        print("\nInterrupted by user.", flush=True)
    except EOFError:
        print("\nEnd of input.", flush=True)


if __name__ == "__main__":
    run_kiro_ide_mode()
