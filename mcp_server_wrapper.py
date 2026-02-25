#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for Kiro Agent
Exposes your agent as an MCP server that Kiro IDE can connect to
"""
import asyncio
import json
import sys
import io
from typing import Any, Dict, Optional
import logging

# Force UTF-8 encoding for stdout/stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Setup logging to stderr (stdout is for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Import agent components
from agent import Agent
from config import load_config


class KiroAgentMCPServer:
    """MCP Server that wraps your Kiro Agent"""
    
    def __init__(self):
        logger.info("Initializing Kiro Agent MCP Server...")
        self.config = None
        self.agent = None
        self.session_id = "mcp-session"
        logger.info("MCP Server initialized (agent will load on first use)")
    
    def _ensure_agent(self):
        """Lazy load agent on first use"""
        if self.agent is None:
            logger.info("Loading agent for first time...")
            
            # Suppress all stdout during agent initialization
            import os
            import sys
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            
            try:
                self.config = load_config()
                self.agent = Agent(self.config)
                logger.info("Agent loaded successfully")
            finally:
                sys.stdout.close()
                sys.stdout = old_stdout
    
    def create_response(self, request_id: Optional[int], result: Any) -> Dict[str, Any]:
        """Create MCP response"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        return response
    
    def create_error(self, request_id: Optional[int], code: int, message: str) -> Dict[str, Any]:
        """Create MCP error response"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        return response
    
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        logger.info("Handling initialize request")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "kiro-agent",
                "version": "0.1.0"
            }
        }
    
    async def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        logger.info("Handling tools/list request")
        
        tools = [
            {
                "name": "chat",
                "description": "Chat with Kiro Agent - ask questions, request code generation, file operations, web searches, etc.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Your message or request to the agent"
                        },
                        "max_iterations": {
                            "type": "number",
                            "description": "Maximum iterations for agentic loop (default: 3)",
                            "default": 3
                        }
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "get_status",
                "description": "Get current agent status and available tools",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        return {"tools": tools}
    
    async def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Handling tools/call: {tool_name}")
        logger.info(f"Arguments: {arguments}")
        
        try:
            # Ensure agent is loaded
            self._ensure_agent()
            
            if tool_name == "chat":
                message = arguments.get("message")
                max_iterations = arguments.get("max_iterations", 3)
                
                logger.info(f"Processing chat message: {message[:50]}...")
                
                # Run agent
                response = self.agent.run(
                    message,
                    stream=False,
                    max_iterations=max_iterations,
                    verbose=False
                )
                
                logger.info(f"Agent response length: {len(response)}")
                
                # Ensure ASCII-safe response
                safe_response = response.encode('ascii', errors='replace').decode('ascii')
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_response
                        }
                    ]
                }
            
            elif tool_name == "get_status":
                status = self.agent.get_status()
                
                status_text = f"""Agent Status:
- Model: {status['model']}
- Tools: {len(status['tools'])} available
- MCP Servers: {len(status['mcp_servers_connected'])} connected
- Conversation: {status['conversation_length']} messages
- Last iteration: {status['last_iteration']}

Available Tools:
{chr(10).join('- ' + tool for tool in status['tools'])}

Connected MCP Servers:
{chr(10).join('- ' + server for server in status['mcp_servers_connected']) if status['mcp_servers_connected'] else '(none)'}
"""
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": status_text
                        }
                    ]
                }
            
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        except Exception as e:
            logger.error(f"Error executing tool: {e}", exc_info=True)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request"""
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})
        
        logger.info(f"Received request: {method}")
        
        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
                return self.create_response(request_id, result)
            
            elif method == "tools/list":
                result = await self.handle_tools_list(params)
                return self.create_response(request_id, result)
            
            elif method == "tools/call":
                result = await self.handle_tools_call(params)
                return self.create_response(request_id, result)
            
            else:
                logger.warning(f"Unknown method: {method}")
                return self.create_error(request_id, -32601, f"Method not found: {method}")
        
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            return self.create_error(request_id, -32603, str(e))
    
    async def run(self):
        """Run MCP server on stdio"""
        logger.info("Starting MCP server on stdio...")
        
        try:
            while True:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    logger.info("EOF received, shutting down")
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = await self.handle_request(request)
                    
                    # Write response to stdout
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    error_response = self.create_error(None, -32700, "Parse error")
                    print(json.dumps(error_response), flush=True)
        
        except KeyboardInterrupt:
            logger.info("Received interrupt, shutting down")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            logger.info("MCP server stopped")


async def main():
    """Main entry point"""
    server = KiroAgentMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
