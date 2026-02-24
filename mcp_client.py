"""
MCP (Model Context Protocol) Client
Handles connection and communication with MCP servers
"""
from typing import Dict, List, Any, Optional
import json
import subprocess
import asyncio
import os
from dataclasses import dataclass
from enum import Enum


class MCPTransportType(Enum):
    """Types of MCP transports"""
    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server"""
    name: str
    command: str  # Command to start the server (for stdio)
    transport: MCPTransportType = MCPTransportType.STDIO
    url: Optional[str] = None  # For HTTP/WebSocket
    args: List[str] = None  # Arguments for the command
    env: Dict[str, str] = None  # Environment variables
    
    def __post_init__(self):
        if self.args is None:
            self.args = []
        if self.env is None:
            self.env = {}


class MCPClient:
    """Client for communicating with MCP servers"""
    
    def __init__(self, server_config: MCPServerConfig):
        """
        Initialize MCP client
        
        Args:
            server_config: Configuration for the MCP server
        """
        self.config = server_config
        self.process = None
        self.connected = False
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self) -> bool:
        """Connect to the MCP server"""
        try:
            if self.config.transport == MCPTransportType.STDIO:
                # Start the server process
                self.process = subprocess.Popen(
                    [self.config.command] + self.config.args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, **self.config.env},
                    text=True,
                    bufsize=1,
                )
                self.connected = True
                await self._initialize()
                return True
            
            elif self.config.transport == MCPTransportType.HTTP:
                # For HTTP/WebSocket, verify connection
                import requests
                response = requests.get(f"{self.config.url}/health", timeout=5)
                self.connected = response.status_code == 200
                if self.connected:
                    await self._initialize()
                return self.connected
            
        except Exception as e:
            print(f"Failed to connect to MCP server {self.config.name}: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.connected = False
    
    async def _initialize(self):
        """Initialize connection - list tools and resources"""
        try:
            await self.list_tools()
            await self.list_resources()
        except Exception as e:
            print(f"Error initializing MCP server: {e}")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the MCP server"""
        try:
            response = await self._send_request("tools/list")
            tools = response.get("tools", [])
            
            # Store tools locally for quick access
            for tool in tools:
                self.tools[tool["name"]] = tool
            
            return tools
        except Exception as e:
            print(f"Error listing tools: {e}")
            return []
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources from the MCP server"""
        try:
            response = await self._send_request("resources/list")
            resources = response.get("resources", [])
            
            # Store resources locally
            for resource in resources:
                self.resources[resource["uri"]] = resource
            
            return resources
        except Exception as e:
            print(f"Error listing resources: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server"""
        try:
            if tool_name not in self.tools:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found"
                }
            
            result = await self._send_request(
                "tools/call",
                {
                    "name": tool_name,
                    "arguments": arguments
                }
            )
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def read_resource(self, uri: str) -> Optional[str]:
        """Read a resource from the MCP server"""
        try:
            result = await self._send_request(
                "resources/read",
                {"uri": uri}
            )
            return result.get("contents")
        except Exception as e:
            print(f"Error reading resource: {e}")
            return None
    
    async def _send_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        if self.config.transport == MCPTransportType.STDIO:
            return await self._send_stdio_request(method, params)
        elif self.config.transport == MCPTransportType.HTTP:
            return await self._send_http_request(method, params)
        else:
            raise NotImplementedError(f"Transport {self.config.transport} not implemented")
    
    async def _send_stdio_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send request via stdio"""
        import json
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }
        
        try:
            # Write request
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()
            
            # Read response
            response_line = self.process.stdout.readline()
            if response_line:
                return json.loads(response_line)
            return {"error": "No response from server"}
        except Exception as e:
            raise RuntimeError(f"STDIO request failed: {e}")
    
    async def _send_http_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send request via HTTP"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params or {},
                "id": 1
            }
            
            async with session.post(
                f"{self.config.url}/rpc",
                json=payload,
                timeout=30
            ) as response:
                return await response.json()


class MCPServerManager:
    """Manages multiple MCP server connections"""
    
    def __init__(self):
        self.clients: Dict[str, MCPClient] = {}
        self.configs: Dict[str, MCPServerConfig] = {}
    
    def register_server(self, config: MCPServerConfig) -> None:
        """Register an MCP server configuration"""
        self.configs[config.name] = config
    
    async def connect_server(self, server_name: str) -> bool:
        """Connect to a registered MCP server"""
        if server_name not in self.configs:
            return False
        
        config = self.configs[server_name]
        client = MCPClient(config)
        
        if await client.connect():
            self.clients[server_name] = client
            return True
        
        return False
    
    async def disconnect_server(self, server_name: str) -> bool:
        """Disconnect from an MCP server"""
        if server_name in self.clients:
            await self.clients[server_name].disconnect()
            del self.clients[server_name]
            return True
        return False
    
    async def disconnect_all(self):
        """Disconnect from all MCP servers"""
        for server_name in list(self.clients.keys()):
            await self.disconnect_server(server_name)
    
    def get_client(self, server_name: str) -> Optional[MCPClient]:
        """Get a connected MCP client"""
        return self.clients.get(server_name)
    
    def list_connected_servers(self) -> List[str]:
        """List all connected MCP servers"""
        return list(self.clients.keys())
    
    def list_available_servers(self) -> List[str]:
        """List all registered MCP servers"""
        return list(self.configs.keys())
    
    async def list_all_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all tools from all connected servers"""
        all_tools = {}
        for server_name, client in self.clients.items():
            all_tools[server_name] = list(client.tools.values())
        return all_tools
    
    async def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a tool on a specific MCP server"""
        client = self.get_client(server_name)
        if not client:
            return {
                "success": False,
                "error": f"Server '{server_name}' not connected"
            }
        
        return await client.call_tool(tool_name, arguments)
