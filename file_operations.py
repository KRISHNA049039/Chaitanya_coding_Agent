"""
File Operations with User Approval
Allows agent to propose file changes that require user approval
"""
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
import os
import difflib
from tools import Tool, ToolResult


@dataclass
class FileChange:
    """Represents a proposed file change"""
    operation: str  # 'create', 'modify', 'delete'
    path: str
    content: Optional[str] = None
    old_content: Optional[str] = None
    reason: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "operation": self.operation,
            "path": self.path,
            "content": self.content,
            "old_content": self.old_content,
            "reason": self.reason
        }
    
    def get_diff(self) -> str:
        """Generate diff for modify operations"""
        if self.operation != "modify" or not self.old_content:
            return ""
        
        old_lines = self.old_content.splitlines(keepends=True)
        new_lines = (self.content or "").splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{self.path}",
            tofile=f"b/{self.path}",
            lineterm=""
        )
        return "".join(diff)


class ApprovalHandler:
    """Handles user approval for file operations"""
    
    def __init__(self):
        self.pending_changes: Dict[str, FileChange] = {}
        self.approval_callback: Optional[Callable] = None
        self.change_id_counter = 0
    
    def set_approval_callback(self, callback: Callable) -> None:
        """Set callback function for requesting approval"""
        self.approval_callback = callback
    
    def request_approval(self, change: FileChange) -> str:
        """Request approval for a file change, returns change_id"""
        self.change_id_counter += 1
        change_id = f"change_{self.change_id_counter}"
        self.pending_changes[change_id] = change
        
        if self.approval_callback:
            self.approval_callback(change_id, change)
        
        return change_id
    
    def approve_change(self, change_id: str) -> ToolResult:
        """Approve and execute a pending change"""
        if change_id not in self.pending_changes:
            return ToolResult(
                success=False,
                output="",
                error=f"Change {change_id} not found"
            )
        
        change = self.pending_changes[change_id]
        result = self._execute_change(change)
        
        if result.success:
            del self.pending_changes[change_id]
        
        return result
    
    def reject_change(self, change_id: str, reason: str = "") -> ToolResult:
        """Reject a pending change"""
        if change_id not in self.pending_changes:
            return ToolResult(
                success=False,
                output="",
                error=f"Change {change_id} not found"
            )
        
        del self.pending_changes[change_id]
        return ToolResult(
            success=True,
            output=f"Change rejected: {reason}" if reason else "Change rejected"
        )
    
    def _normalize_path(self, path: str) -> str:
        """Normalize file path to prevent absolute path issues"""
        # Remove leading slashes to make path relative
        normalized = path.lstrip('/')
        normalized = path.lstrip('\\')
        
        # Prevent directory traversal attacks
        if '..' in normalized:
            raise ValueError("Path traversal not allowed")
        
        return normalized
    
    def _execute_change(self, change: FileChange) -> ToolResult:
        """Execute the actual file operation"""
        try:
            # Normalize path for file operations (not for shell commands)
            if change.operation != "execute_shell":
                try:
                    change.path = self._normalize_path(change.path)
                except ValueError as e:
                    return ToolResult(
                        success=False,
                        output="",
                        error=f"Invalid path: {str(e)}"
                    )
            
            if change.operation == "execute_shell":
                # Import here to avoid circular dependency
                from shell_tool import execute_shell_command
                return execute_shell_command(change.path)  # command is stored in path
            
            elif change.operation == "create":
                # Check if file already exists
                if os.path.exists(change.path):
                    return ToolResult(
                        success=False,
                        output="",
                        error=f"File already exists: {change.path}"
                    )
                
                # Get directory path
                dir_path = os.path.dirname(change.path)
                
                # Create directory if needed (only if path has a directory component)
                if dir_path and dir_path != '':
                    os.makedirs(dir_path, exist_ok=True)
                
                # Write file
                with open(change.path, 'w', encoding='utf-8') as f:
                    f.write(change.content or "")
                
                # Get absolute path for display
                abs_path = os.path.abspath(change.path)
                return ToolResult(
                    success=True,
                    output=f"Created file: {abs_path}"
                )
            
            elif change.operation == "modify":
                if not os.path.exists(change.path):
                    return ToolResult(
                        success=False,
                        output="",
                        error=f"File not found: {change.path}"
                    )
                
                with open(change.path, 'w', encoding='utf-8') as f:
                    f.write(change.content or "")
                
                return ToolResult(
                    success=True,
                    output=f"Modified file: {change.path}"
                )
            
            elif change.operation == "delete":
                if not os.path.exists(change.path):
                    return ToolResult(
                        success=False,
                        output="",
                        error=f"File not found: {change.path}"
                    )
                
                os.remove(change.path)
                return ToolResult(
                    success=True,
                    output=f"Deleted file: {change.path}"
                )
            
            else:
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Unknown operation: {change.operation}"
                )
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Error executing change: {str(e)}"
            )


# Global approval handler instance
approval_handler = ApprovalHandler()


class CreateFileTool(Tool):
    """Tool for creating new files with approval"""
    
    def __init__(self, approval_handler: ApprovalHandler):
        super().__init__(
            name="create_file",
            description="Propose creating a new file (requires user approval). Parameters: path (file path), content (file content), reason (optional explanation)"
        )
        self.approval_handler = approval_handler
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - File path to create (e.g., 'src/utils.py')",
                "content": "string - Content to write to the file",
                "reason": "string (optional) - Reason for creating the file"
            }
        }
    
    def execute(self, path: str, content: str, reason: str = "") -> ToolResult:
        """Propose file creation"""
        change = FileChange(
            operation="create",
            path=path,
            content=content,
            reason=reason or f"Create new file: {path}"
        )
        
        change_id = self.approval_handler.request_approval(change)
        
        return ToolResult(
            success=True,
            output=f"File creation proposed (ID: {change_id}). Waiting for user approval..."
        )


class ModifyFileTool(Tool):
    """Tool for modifying existing files with approval"""
    
    def __init__(self, approval_handler: ApprovalHandler):
        super().__init__(
            name="modify_file",
            description="Propose modifying an existing file (requires user approval). Parameters: path (file path), content (new content), reason (optional explanation)"
        )
        self.approval_handler = approval_handler
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - File path to modify (e.g., 'src/main.py')",
                "content": "string - New content for the file",
                "reason": "string (optional) - Reason for modifying the file"
            }
        }
    
    def execute(self, path: str, content: str, reason: str = "") -> ToolResult:
        """Propose file modification"""
        # Read current content
        old_content = ""
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            except Exception as e:
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Error reading file: {str(e)}"
                )
        else:
            return ToolResult(
                success=False,
                output="",
                error=f"File not found: {path}"
            )
        
        change = FileChange(
            operation="modify",
            path=path,
            content=content,
            old_content=old_content,
            reason=reason or f"Modify file: {path}"
        )
        
        change_id = self.approval_handler.request_approval(change)
        
        return ToolResult(
            success=True,
            output=f"File modification proposed (ID: {change_id}). Waiting for user approval..."
        )


class DeleteFileTool(Tool):
    """Tool for deleting files with approval"""
    
    def __init__(self, approval_handler: ApprovalHandler):
        super().__init__(
            name="delete_file",
            description="Propose deleting a file (requires user approval). Parameters: path (file path), reason (optional explanation)"
        )
        self.approval_handler = approval_handler
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - File path to delete (e.g., 'temp/old_file.txt')",
                "reason": "string (optional) - Reason for deleting the file"
            }
        }
    
    def execute(self, path: str, reason: str = "") -> ToolResult:
        """Propose file deletion"""
        if not os.path.exists(path):
            return ToolResult(
                success=False,
                output="",
                error=f"File not found: {path}"
            )
        
        change = FileChange(
            operation="delete",
            path=path,
            reason=reason or f"Delete file: {path}"
        )
        
        change_id = self.approval_handler.request_approval(change)
        
        return ToolResult(
            success=True,
            output=f"File deletion proposed (ID: {change_id}). Waiting for user approval..."
        )


class ListDirectoryTool(Tool):
    """Tool for listing directory contents"""
    
    def __init__(self):
        super().__init__(
            name="list_directory",
            description="List files and directories in a path. Parameters: path (directory path, default '.'), recursive (boolean, default false)"
        )
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string (optional) - Directory path to list (default: current directory)",
                "recursive": "boolean (optional) - List recursively (default: false)"
            }
        }
    
    def execute(self, path: str = ".", recursive: bool = False) -> ToolResult:
        """List directory contents"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Path not found: {path}"
                )
            
            if not os.path.isdir(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Not a directory: {path}"
                )
            
            if recursive:
                items = []
                for root, dirs, files in os.walk(path):
                    level = root.replace(path, '').count(os.sep)
                    indent = ' ' * 2 * level
                    items.append(f"{indent}{os.path.basename(root)}/")
                    subindent = ' ' * 2 * (level + 1)
                    for file in files:
                        items.append(f"{subindent}{file}")
                output = '\n'.join(items)
            else:
                items = os.listdir(path)
                items.sort()
                output = '\n'.join(items)
            
            return ToolResult(success=True, output=output)
        
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=str(e)
            )
