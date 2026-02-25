"""
CLI Chat Interface with Streaming
Interactive command-line chat with the agent
"""
import asyncio
import sys
from typing import Optional
from colorama import init, Fore, Style
import uuid

from agent import Agent
from config import load_config
from file_operations import approval_handler

# Initialize colorama for Windows
init()


class CLIChat:
    """Command-line chat interface"""
    
    def __init__(self):
        self.config = load_config()
        self.agent = None
        self.session_id = str(uuid.uuid4())
        self.pending_approvals = {}
        
    def setup_approval_handler(self):
        """Setup approval callback for file operations"""
        def approval_callback(change_id: str, change):
            self.pending_approvals[change_id] = change
            self.print_approval_request(change_id, change)
        
        approval_handler.set_approval_callback(approval_callback)
    
    def print_approval_request(self, change_id: str, change):
        """Print approval request to console"""
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"📋 APPROVAL REQUIRED: {change_id}")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Operation:{Style.RESET_ALL} {change.operation}")
        print(f"{Fore.CYAN}Path:{Style.RESET_ALL} {change.path}")
        
        if change.reason:
            print(f"{Fore.CYAN}Reason:{Style.RESET_ALL} {change.reason}")
        
        if change.operation == "create":
            print(f"\n{Fore.GREEN}Content:{Style.RESET_ALL}")
            print(change.content[:500] + "..." if len(change.content or "") > 500 else change.content)
        
        elif change.operation == "modify":
            print(f"\n{Fore.YELLOW}Diff:{Style.RESET_ALL}")
            print(change.get_diff()[:500])
        
        print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
        print(f"  approve {change_id} - Approve this change")
        print(f"  reject {change_id} - Reject this change")
        print(f"{'='*60}\n")
    
    async def initialize(self):
        """Initialize agent and MCP servers"""
        print(f"{Fore.CYAN}🚀 Initializing Kiro Agent...{Style.RESET_ALL}")
        
        try:
            self.agent = Agent(self.config)
            self.setup_approval_handler()
            
            # Auto-connect MCP servers
            if self.config.enable_mcp:
                print(f"{Fore.CYAN}🔌 Connecting MCP servers...{Style.RESET_ALL}")
                results = await self.agent.auto_connect_mcp_servers()
                for server, success in results.items():
                    status = f"{Fore.GREEN}✓" if success else f"{Fore.RED}✗"
                    print(f"  {status} {server}{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}✓ Agent ready!{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error initializing agent: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def print_welcome(self):
        """Print welcome message"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"  🤖 Kiro Agent - CLI Chat")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"Model: {self.config.llm_config.model_name}")
        print(f"Session: {self.session_id[:8]}...")
        print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
        print(f"  /help - Show help")
        print(f"  /clear - Clear conversation")
        print(f"  /tools - List available tools")
        print(f"  /exit - Exit chat")
        print(f"  approve <id> - Approve pending change")
        print(f"  reject <id> - Reject pending change")
        print(f"{'='*60}\n")
    
    def handle_command(self, command: str) -> bool:
        """Handle special commands, returns True if should continue"""
        if command == "/exit":
            print(f"{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
            return False
        
        elif command == "/help":
            self.print_welcome()
        
        elif command == "/clear":
            self.agent.conversation_history.clear()
            print(f"{Fore.GREEN}✓ Conversation cleared{Style.RESET_ALL}")
        
        elif command == "/tools":
            print(f"\n{Fore.CYAN}Available Tools:{Style.RESET_ALL}")
            for tool_name in self.agent.tools.list_tools():
                print(f"  • {tool_name}")
            print()
        
        elif command.startswith("approve "):
            change_id = command.split()[1]
            result = approval_handler.approve_change(change_id)
            if result.success:
                print(f"{Fore.GREEN}✓ {result.output}{Style.RESET_ALL}")
                del self.pending_approvals[change_id]
            else:
                print(f"{Fore.RED}✗ {result.error}{Style.RESET_ALL}")
        
        elif command.startswith("reject "):
            change_id = command.split()[1]
            result = approval_handler.reject_change(change_id)
            print(f"{Fore.YELLOW}{result.output}{Style.RESET_ALL}")
            if change_id in self.pending_approvals:
                del self.pending_approvals[change_id]
        
        else:
            print(f"{Fore.RED}Unknown command. Type /help for help.{Style.RESET_ALL}")
        
        return True
    
    async def chat_loop(self):
        """Main chat loop"""
        while True:
            try:
                # Get user input
                user_input = input(f"{Fore.GREEN}You:{Style.RESET_ALL} ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith("/") or user_input.startswith("approve ") or user_input.startswith("reject "):
                    if not self.handle_command(user_input):
                        break
                    continue
                
                # Send to agent
                print(f"\n{Fore.CYAN}Agent:{Style.RESET_ALL} ", end="", flush=True)
                
                response = self.agent.run(user_input, stream=True)
                
                # Print streaming response
                if hasattr(response, '__iter__') and not isinstance(response, str):
                    # It's a generator - stream it!
                    for chunk in response:
                        print(chunk, end="", flush=True)
                else:
                    # It's a string - print it
                    print(response)
                
                print("\n")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use /exit to quit{Style.RESET_ALL}")
            except EOFError:
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}\n")
    
    async def run(self):
        """Run the CLI chat"""
        await self.initialize()
        self.print_welcome()
        await self.chat_loop()


async def main():
    """Main entry point"""
    chat = CLIChat()
    await chat.run()


if __name__ == "__main__":
    asyncio.run(main())
