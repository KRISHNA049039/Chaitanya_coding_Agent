"""
CLI Interface for Kiro AI Agent
"""
import typer
from typing import Optional
from colorama import Fore, Style, init
import sys
import asyncio
import io
import json

# Force unbuffered output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

from agent import Agent
from config import load_config, MCPServerConfig
from mcp_client import MCPTransportType

# Initialize colorama for cross-platform colored text
init(autoreset=True)

app = typer.Typer(help="Kiro - AI Agent with Local LLM Integration and MCP Support")


def print_welcome():
    """Print welcome message"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Welcome to Kiro - Local AI Agent")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def print_status(agent: Agent):
    """Print agent status"""
    status = agent.get_status()
    print(f"\n{Fore.GREEN}Agent Status:{Style.RESET_ALL}")
    print(f"  Name: {status['agent_name']}")
    print(f"  Model: {Fore.YELLOW}{status['model']}{Style.RESET_ALL}")
    print(f"  LLM URL: {status['llm_url']}")
    print(f"  Tools: {', '.join(status['tools'])}")
    print()


@app.command()
def chat(
    message: Optional[str] = typer.Argument(None, help="Message to send to agent (optional, enters interactive mode if omitted)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Chat with the Kiro agent in interactive mode
    
    Examples:
        kiro chat                  # Interactive mode
        kiro chat "hello"          # Single message and exit
        kiro chat "hello" --verbose
    """
    try:
        config = load_config()
        agent = Agent(config=config)
        
        # Setup approval bridge for VS Code integration
        from approval_bridge import setup_approval_callback, approval_bridge
        setup_approval_callback(agent.approval_handler)
        
        # Check if stdin is a TTY (interactive terminal)
        is_interactive = sys.stdin.isatty()
        
        # Only print welcome/status in interactive mode
        if is_interactive:
            print_welcome()
            print_status(agent)
        
        # Always start in interactive mode unless message is provided
        # After a single message, offer to continue chatting
        if message:
            if is_interactive:
                print(f"{Fore.GREEN}You: {Style.RESET_ALL}{message}\n")
                print(f"{Fore.BLUE}Agent thinking...{Style.RESET_ALL}\n")
            response = agent.run(message, verbose=verbose)
            print(f"{Fore.CYAN}Kiro:{Style.RESET_ALL}\n{response}\n", flush=True)
            # Ask if user wants to continue
            message = None
        
        # Interactive mode only if stdin is a TTY
        if not is_interactive:
            # Non-interactive mode: read from stdin line by line (for VS Code extension)
            print("ready", flush=True)
            for line in sys.stdin:
                user_input = line.strip()
                
                # Check for approval responses from VS Code
                if user_input.startswith('APPROVAL_RESPONSE:'):
                    try:
                        response_data = json.loads(user_input[len('APPROVAL_RESPONSE:'):])
                        approval_bridge.handle_approval_response(response_data)
                        
                        # Execute the approval/rejection
                        change_id = response_data.get('change_id')
                        approved = response_data.get('approved', False)
                        
                        if approved:
                            result = agent.approval_handler.approve_change(change_id)
                        else:
                            result = agent.approval_handler.reject_change(change_id)
                        
                        print(result.output if result.success else result.error, flush=True)
                        continue
                    except Exception as e:
                        print(f"Error handling approval: {e}", flush=True)
                        continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                response = agent.run(user_input, verbose=verbose)
                print(f"{response}\n", flush=True)
            return
        
        # Interactive mode
        print(f"{Fore.CYAN}Interactive mode. Type 'exit' to quit.{Style.RESET_ALL}\n")
        while True:
            try:
                user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}\n")
                    break
                
                if not user_input:
                    continue
                
                print(f"\n{Fore.BLUE}Agent thinking...{Style.RESET_ALL}\n")
                response = agent.run(user_input, verbose=verbose)
                print(f"{Fore.CYAN}Kiro: {Style.RESET_ALL}{response}\n", flush=True)
            
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}\n")
                break
    
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n", flush=True)
        sys.exit(1)


@app.command()
def status():
    """Check agent and LLM status"""
    try:
        config = load_config()
        agent = Agent(config=config)
        
        print_welcome()
        print_status(agent)
        
        print(f"{Fore.GREEN}✅ Agent is ready!{Style.RESET_ALL}\n")
        print(f"Configuration:")
        print(f"  Model: {Fore.YELLOW}{config.llm_config.model_name}{Style.RESET_ALL}")
        print(f"  Temperature: {config.llm_config.temperature}")
        print(f"  Max Tokens: {config.llm_config.max_tokens}")
        print(f"\nAvailable Models on LLM Service:")
        
        models = agent.llm.list_models()
        if models:
            for model in models:
                print(f"  - {Fore.YELLOW}{model}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}(Could not retrieve model list){Style.RESET_ALL}")
        
        print()
    
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


@app.command()
def code(
    prompt: str = typer.Argument(..., help="Code generation prompt"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Generate code using the agent
    
    Examples:
        kiro code "write a function to calculate fibonacci"
        kiro code "create a REST API endpoint" --verbose
    """
    try:
        config = load_config()
        agent = Agent(config=config)
        
        print_welcome()
        print(f"{Fore.GREEN}Prompt: {Style.RESET_ALL}{prompt}\n")
        print(f"{Fore.BLUE}Agent generating code...{Style.RESET_ALL}\n")
        
        response = agent.run(prompt, verbose=verbose)
        print(f"{Fore.CYAN}Generated Code:{Style.RESET_ALL}\n{response}\n")
    
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


@app.command()
def setup():
    """Setup and test the agent"""
    print_welcome()
    print(f"{Fore.YELLOW}Setting up Kiro Agent...{Style.RESET_ALL}\n")
    
    # Check environment
    print("Checking environment...")
    try:
        import ollama
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Ollama module found")
    except ImportError:
        print(f"{Fore.YELLOW}! Ollama module not found{Style.RESET_ALL}")
    
    # Test LLM connection
    try:
        config = load_config()
        agent = Agent(config=config)
        
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} LLM service is running")
        print(f"  URL: {config.llm_config.base_url}")
        print(f"  Model: {config.llm_config.model_name}")
        
        # Test simple chat
        print(f"\n{Fore.BLUE}Testing agent...{Style.RESET_ALL}\n")
        response = agent.simple_chat("Say hello in one word")
        print(f"Agent: {response}\n")
        
        # Test MCP if configured
        if config.mcp_servers:
            print(f"\n{Fore.BLUE}Configuring MCP servers...{Style.RESET_ALL}\n")
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(agent.auto_connect_mcp_servers())
            
            for server_name, success in results.items():
                if success:
                    print(f"{Fore.GREEN}✓{Style.RESET_ALL} MCP server '{server_name}' connected")
                else:
                    print(f"{Fore.YELLOW}! MCP server '{server_name}' failed to connect{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✅ Setup successful! Agent is ready to use.{Style.RESET_ALL}\n")
        print("Usage Examples:")
        print(f"  {Fore.CYAN}kiro chat{Style.RESET_ALL}  - Start interactive chat")
        print(f"  {Fore.CYAN}kiro chat \"your prompt\"{Style.RESET_ALL}  - Send a single message")
        print(f"  {Fore.CYAN}kiro code \"write a script\"{Style.RESET_ALL}  - Generate code")
        print(f"  {Fore.CYAN}kiro status{Style.RESET_ALL}  - Check agent status")
        print(f"  {Fore.CYAN}kiro mcp-list{Style.RESET_ALL}  - List MCP servers")
        print(f"  {Fore.CYAN}kiro mcp-add name command{Style.RESET_ALL}  - Add MCP server\n")
    
    except Exception as e:
        print(f"\n{Fore.RED}Setup failed: {str(e)}{Style.RESET_ALL}\n")
        print("Make sure you have Ollama running:")
        print(f"  {Fore.YELLOW}brew install ollama{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}ollama serve{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}ollama pull mistral{Style.RESET_ALL}\n")
        sys.exit(1)


@app.callback()
def main(
    version: bool = typer.Option(None, "--version", "-v", help="Show version"),
):
    """Kiro - AI Agent with Local LLM Integration and MCP Support"""
    if version:
        print("Kiro v1.0.0 with MCP Support")
        raise typer.Exit()


@app.command()
def mcp_add(
    name: str = typer.Argument(..., help="Name for the MCP server"),
    command: str = typer.Argument(..., help="Command to start the server"),
    transport: str = typer.Option("stdio", "--transport", "-t", help="Transport type: stdio, http, websocket"),
    url: Optional[str] = typer.Option(None, "--url", "-u", help="Base URL for HTTP/WebSocket servers"),
):
    """
    Add an MCP server configuration
    
    Examples:
        kiro mcp-add my-server "python -m my_mcp_server"
        kiro mcp-add web-api "http://localhost:8000" --transport http --url http://localhost:8000
    """
    try:
        config = load_config()
        agent = Agent(config=config)
        
        mcp_config = MCPServerConfig(
            name=name,
            command=command,
            transport=transport,
            url=url,
            enabled=True
        )
        
        agent.add_mcp_server(mcp_config)
        print(f"{Fore.GREEN}✓ MCP server '{name}' added to configuration{Style.RESET_ALL}\n")
        print(f"Details:")
        print(f"  Name: {name}")
        print(f"  Command: {command}")
        print(f"  Transport: {transport}")
        if url:
            print(f"  URL: {url}")
        print()
    
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


@app.command()
def mcp_connect(
    server_name: str = typer.Argument(..., help="Name of the MCP server to connect"),
):
    """Connect to an MCP server"""
    try:
        config = load_config()
        agent = Agent(config=config)
        
        print(f"{Fore.BLUE}Connecting to MCP server '{server_name}'...{Style.RESET_ALL}\n")
        
        # Run async connection
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(agent.connect_mcp_server(server_name))
        
        if success:
            client = agent.mcp_manager.get_client(server_name)
            print(f"{Fore.GREEN}✓ Connected to '{server_name}'{Style.RESET_ALL}\n")
            
            if client and client.tools:
                print(f"Available tools ({len(client.tools)}):")
                for tool_name in client.tools:
                    print(f"  - {tool_name}")
            print()
        else:
            print(f"{Fore.RED}✗ Failed to connect to '{server_name}'{Style.RESET_ALL}\n")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


@app.command()
def mcp_list():
    """List MCP servers"""
    try:
        config = load_config()
        agent = Agent(config=config)
        
        print(f"\n{Fore.CYAN}MCP Servers:{Style.RESET_ALL}\n")
        
        available = agent.mcp_manager.list_available_servers()
        connected = agent.mcp_manager.list_connected_servers()
        
        if available:
            print(f"Configured servers:")
            for server in available:
                status = f"{Fore.GREEN}connected{Style.RESET_ALL}" if server in connected else f"{Fore.YELLOW}not connected{Style.RESET_ALL}"
                print(f"  - {server} ({status})")
        else:
            print(f"{Fore.YELLOW}No MCP servers configured{Style.RESET_ALL}")
        
        print()
    
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


@app.command()
def mcp_tools(
    server_name: Optional[str] = typer.Argument(None, help="MCP server name (optional)"),
):
    """List tools from MCP servers"""
    try:
        config = load_config()
        agent = Agent(config=config)
        
        print(f"\n{Fore.CYAN}MCP Tools:{Style.RESET_ALL}\n")
        
        if server_name:
            # List tools from specific server
            client = agent.mcp_manager.get_client(server_name)
            if not client:
                print(f"{Fore.RED}Server '{server_name}' not connected{Style.RESET_ALL}\n")
                sys.exit(1)
            
            print(f"Tools from '{server_name}':")
            for tool_name, tool_schema in client.tools.items():
                description = tool_schema.get("description", "No description")
                print(f"  - {tool_name}: {description}")
        else:
            # List tools from all servers
            loop = asyncio.get_event_loop()
            all_tools = loop.run_until_complete(agent.mcp_manager.list_all_tools())
            
            if all_tools:
                for server_name, tools in all_tools.items():
                    print(f"Tools from '{server_name}':")
                    for tool_schema in tools:
                        tool_name = tool_schema.get("name")
                        description = tool_schema.get("description", "No description")
                        print(f"  - {tool_name}: {description}")
                    print()
            else:
                print(f"{Fore.YELLOW}No MCP servers connected{Style.RESET_ALL}\n")
    
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


if __name__ == "__main__":
    app()
