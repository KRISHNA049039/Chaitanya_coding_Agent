"""
Shell Command Execution Tool with Approval
Allows agent to execute shell commands with user approval
"""
import subprocess
import os
from typing import Optional
from tools import Tool, ToolResult
from file_operations import FileChange, ApprovalHandler


class ShellCommandTool(Tool):
    """Tool for executing shell commands with approval"""
    
    def __init__(self, approval_handler: ApprovalHandler):
        super().__init__(
            name="execute_shell",
            description="Execute shell command (requires user approval). Parameters: command (shell command), reason (why executing)"
        )
        self.approval_handler = approval_handler
    
    def schema(self):
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "command": "string - Shell command to execute (e.g., 'git status', 'npm install')",
                "reason": "string (optional) - Reason for executing the command"
            }
        }
    
    def execute(self, command: str, reason: str = "") -> ToolResult:
        """Propose shell command execution"""
        # Create a special FileChange for shell commands
        change = FileChange(
            operation="execute_shell",
            path=command,  # Store command in path field
            content=None,
            old_content=None,
            reason=reason or f"Execute shell command: {command}"
        )
        
        change_id = self.approval_handler.request_approval(change)
        
        return ToolResult(
            success=True,
            output=f"Shell command proposed (ID: {change_id}). Waiting for user approval..."
        )


def execute_shell_command(command: str, timeout: int = 30, cwd: Optional[str] = None) -> ToolResult:
    """
    Actually execute the shell command after approval
    This is called by the approval handler
    """
    try:
        # Security: Basic command validation
        dangerous_commands = ['rm -rf /', 'format', 'del /f', 'shutdown', 'reboot']
        if any(dangerous in command.lower() for dangerous in dangerous_commands):
            return ToolResult(
                success=False,
                output="",
                error="Dangerous command blocked for safety"
            )
        
        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd or os.getcwd()
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        
        return ToolResult(
            success=result.returncode == 0,
            output=output.strip() if output else "Command executed successfully (no output)",
            error=None if result.returncode == 0 else f"Command failed with exit code {result.returncode}"
        )
    
    except subprocess.TimeoutExpired:
        return ToolResult(
            success=False,
            output="",
            error=f"Command timed out after {timeout}s"
        )
    except Exception as e:
        return ToolResult(
            success=False,
            output="",
            error=f"Error executing command: {str(e)}"
        )
