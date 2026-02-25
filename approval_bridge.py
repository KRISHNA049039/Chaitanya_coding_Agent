"""
Approval Bridge for VS Code Extension
Handles communication between agent and VS Code for file operation approvals
"""
import json
import sys
from typing import Optional, Dict
from file_operations import FileChange


class ApprovalBridge:
    """Bridge for handling approval requests in VS Code extension mode"""
    
    def __init__(self):
        self.pending_responses: Dict[str, bool] = {}
        self.is_vscode_mode = not sys.stdin.isatty()
    
    def request_approval(self, change_id: str, change: FileChange) -> None:
        """Send approval request to VS Code extension"""
        if not self.is_vscode_mode:
            return
        
        approval_request = {
            "change_id": change_id,
            "change": change.to_dict()
        }
        
        # Send to VS Code extension via stdout
        print(f"APPROVAL_REQUEST:{json.dumps(approval_request)}", flush=True)
    
    def wait_for_approval(self, change_id: str, timeout: int = 300) -> Optional[bool]:
        """Wait for approval response from VS Code extension"""
        if not self.is_vscode_mode:
            return None
        
        # In VS Code mode, the response will come via stdin
        # The CLI will handle this and store in pending_responses
        # For now, return None to indicate waiting
        return self.pending_responses.get(change_id)
    
    def handle_approval_response(self, response_data: Dict) -> None:
        """Handle approval response from VS Code"""
        change_id = response_data.get("change_id")
        approved = response_data.get("approved", False)
        
        if change_id:
            self.pending_responses[change_id] = approved


# Global bridge instance
approval_bridge = ApprovalBridge()


def setup_approval_callback(approval_handler):
    """Setup approval callback to use the bridge"""
    def approval_callback(change_id: str, change: FileChange):
        approval_bridge.request_approval(change_id, change)
    
    approval_handler.set_approval_callback(approval_callback)
