"""
Tool/Plugin System for AI Agent
Allows agent to execute various tasks and tools
"""
from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass
import json
import subprocess
import os
import asyncio


@dataclass
class ToolResult:
    """Result from tool execution"""
    success: bool
    output: str
    error: Optional[str] = None


class Tool:
    """Base class for agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        raise NotImplementedError
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
        }


class MCPTool(Tool):
    """Tool that wraps an MCP server tool"""
    
    def __init__(self, server_name: str, tool_name: str, tool_schema: Dict[str, Any], mcp_manager):
        self.server_name = server_name
        self.tool_name = tool_name
        self.tool_schema = tool_schema
        self.mcp_manager = mcp_manager
        
        super().__init__(
            name=f"{server_name}/{tool_name}",
            description=tool_schema.get("description", f"Tool {tool_name} from {server_name}")
        )
    
    def execute(self, **kwargs) -> ToolResult:
        """Execute MCP tool"""
        try:
            # Create event loop if needed
            loop = None
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run async call
            result = loop.run_until_complete(
                self.mcp_manager.call_tool(
                    self.server_name,
                    self.tool_name,
                    kwargs
                )
            )
            
            if result.get("success", True):
                return ToolResult(
                    success=True,
                    output=json.dumps(result.get("output", result))
                )
            else:
                return ToolResult(
                    success=False,
                    output="",
                    error=result.get("error", "Unknown error")
                )
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=str(e)
            )


class CodeExecutionTool(Tool):
    """Tool for executing Python code"""
    
    def __init__(self):
        super().__init__(
            name="execute_code",
            description="Execute Python code and get output. Parameters: code (Python code string), timeout (optional, default 30 seconds)"
        )
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "code": "string - Python code to execute",
                "timeout": "integer (optional) - Timeout in seconds (default: 30)"
            }
        }
    
    def execute(self, code: str, timeout: int = 30) -> ToolResult:
        """Execute Python code safely"""
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return ToolResult(
                    success=True,
                    output=result.stdout.strip()
                )
            else:
                return ToolResult(
                    success=False,
                    output="",
                    error=result.stderr.strip()
                )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output="",
                error=f"Code execution timed out after {timeout}s"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=str(e)
            )


class FileTool(Tool):
    """Tool for reading files"""
    
    def __init__(self):
        super().__init__(
            name="read_file",
            description="Read contents of a file. Parameters: path (file path), max_lines (optional, limit number of lines)"
        )
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "path": "string - Path to file to read (e.g., 'config.py')",
                "max_lines": "integer (optional) - Maximum number of lines to read"
            }
        }
    
    def execute(self, path: str, max_lines: Optional[int] = None) -> ToolResult:
        """Read file contents"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"File not found: {path}"
                )
            
            with open(path, 'r') as f:
                content = f.read()
            
            if max_lines:
                lines = content.split('\n')[:max_lines]
                content = '\n'.join(lines)
            
            return ToolResult(success=True, output=content)
        except Exception as e:
            return ToolResult(
                success=False,
                output="",
                error=str(e)
            )


class ShellTool(Tool):
    """Tool for executing shell commands"""
    
    def __init__(self):
        super().__init__(
            name="execute_command",
            description="Execute shell command. Parameters: command (shell command string), timeout (optional, default 30 seconds)"
        )
    
    def schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "command": "string - Shell command to execute",
                "timeout": "integer (optional) - Timeout in seconds (default: 30)"
            }
        }
    
    def execute(self, command: str, timeout: int = 30) -> ToolResult:
        """Execute shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return ToolResult(success=True, output=result.stdout.strip())
            else:
                return ToolResult(
                    success=False,
                    output="",
                    error=result.stderr.strip()
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
                error=str(e)
            )


class ToolRegistry:
    """Registry for managing agent tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.mcp_manager = None  # Will be set by agent
    
    def set_mcp_manager(self, mcp_manager) -> None:
        """Set the MCP manager for MCP tools"""
        self.mcp_manager = mcp_manager
    
    def register(self, tool: Tool) -> None:
        """Register a tool"""
        self.tools[tool.name] = tool
    
    def register_mcp_tools(self, server_name: str, tools: List[Dict[str, Any]]) -> None:
        """Register tools from an MCP server"""
        if not self.mcp_manager:
            return
        
        for tool_schema in tools:
            tool_name = tool_schema.get("name")
            if tool_name:
                mcp_tool = MCPTool(server_name, tool_name, tool_schema, self.mcp_manager)
                self.register(mcp_tool)
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())
    
    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """Execute a tool"""
        tool = self.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                output="",
                error=f"Tool not found: {tool_name}"
            )
        return tool.execute(**kwargs)
    
    def get_tools_description(self) -> str:
        """Get formatted description of all tools"""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)


def create_default_registry(approval_handler=None) -> ToolRegistry:
    """Create registry with default tools"""
    registry = ToolRegistry()
    registry.register(CodeExecutionTool())
    registry.register(FileTool())
    registry.register(ShellTool())
    
    # Add web search tools (no approval needed)
    from web_search_tool import WebSearchTool, FetchURLTool, QuickAnswerTool
    registry.register(WebSearchTool())
    registry.register(FetchURLTool())
    registry.register(QuickAnswerTool())
    
    # Add PDF tools (no approval needed)
    try:
        from pdf_tools import PDFReaderTool, PDFInfoTool, PDFSearchTool, ScanDirectoryForPDFsTool
        registry.register(PDFReaderTool())
        registry.register(PDFInfoTool())
        registry.register(PDFSearchTool())
        registry.register(ScanDirectoryForPDFsTool())
    except ImportError:
        print("Warning: PDF tools not available (install PyPDF2)")
    
    # Add semantic search tools (no approval needed)
    try:
        from semantic_search_tool import SemanticSearchTool, CodeSearchTool
        registry.register(SemanticSearchTool())
        registry.register(CodeSearchTool())
    except ImportError:
        print("Warning: Semantic search not available (install sentence-transformers)")
    
    # Add file operation tools with approval if handler provided
    if approval_handler:
        from file_operations import (
            CreateFileTool, ModifyFileTool, DeleteFileTool, ListDirectoryTool
        )
        from shell_tool import ShellCommandTool
        
        registry.register(CreateFileTool(approval_handler))
        registry.register(ModifyFileTool(approval_handler))
        registry.register(DeleteFileTool(approval_handler))
        registry.register(ListDirectoryTool())
        registry.register(ShellCommandTool(approval_handler))
    
    return registry
