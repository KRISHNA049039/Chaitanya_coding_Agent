"""
Example Usage of Kiro AI Agent
Shows how to use the agent in your own code, including MCP integration
"""
import asyncio
from agent import Agent
from config import AgentConfig, LLMConfig, MCPServerConfig
from tools import ToolRegistry, CodeExecutionTool, FileTool, ShellTool


def example_basic_chat():
    """Example 1: Basic chat without tools"""
    print("=" * 60)
    print("Example 1: Basic Chat")
    print("=" * 60)
    
    agent = Agent()
    response = agent.simple_chat("What is the capital of France?")
    print(f"Agent: {response}\n")


def example_agentic_loop():
    """Example 2: Agent with tool usage"""
    print("=" * 60)
    print("Example 2: Agentic Loop with Tools")
    print("=" * 60)
    
    agent = Agent()
    
    # Example that might use tools
    prompt = "Write a Python function that adds two numbers and test it"
    
    print(f"User: {prompt}\n")
    response = agent.run(prompt, verbose=True)
    print(f"\nFinal Response: {response}\n")


def example_custom_config():
    """Example 3: Custom configuration"""
    print("=" * 60)
    print("Example 3: Custom Configuration")
    print("=" * 60)
    
    # Create custom config
    config = AgentConfig(
        llm_config=LLMConfig(
            model_name="neural-chat",  # Different model
            temperature=0.5,  # More deterministic
            max_tokens=1024,
        ),
        max_iterations=5,  # Limit iterations
    )
    
    agent = Agent(config=config)
    response = agent.simple_chat("Explain machine learning briefly")
    print(f"Agent: {response}\n")


def example_conversation():
    """Example 4: Multi-turn conversation"""
    print("=" * 60)
    print("Example 4: Multi-turn Conversation")
    print("=" * 60)
    
    agent = Agent()
    
    # First turn
    from llm_client import Message
    agent.conversation_history.append(
        Message(role="user", content="What is Python?")
    )
    
    response1 = agent.llm.chat(
        messages=agent.conversation_history,
        system_prompt=agent._build_system_prompt(),
    )
    print(f"Assistant: {response1[:200]}...")
    agent.conversation_history.append(
        Message(role="assistant", content=response1)
    )
    
    # Second turn
    agent.conversation_history.append(
        Message(role="user", content="What are its main features?")
    )
    
    response2 = agent.llm.chat(
        messages=agent.conversation_history,
        system_prompt=agent._build_system_prompt(),
    )
    print(f"Assistant: {response2[:200]}...\n")


def example_mcp_setup():
    """Example 5: Setup and use MCP servers"""
    print("=" * 60)
    print("Example 5: MCP Server Integration")
    print("=" * 60)
    
    config = AgentConfig()
    agent = Agent(config=config)
    
    # Register an MCP server
    mcp_config = MCPServerConfig(
        name="example-server",
        command="python -m my_mcp_server",  # Your MCP server command
        transport="stdio",
        enabled=True
    )
    
    agent.add_mcp_server(mcp_config)
    
    print(f"Available MCP servers: {agent.mcp_manager.list_available_servers()}")
    
    # To connect: (requires async context)
    # loop = asyncio.get_event_loop()
    # success = loop.run_until_complete(agent.connect_mcp_server("example-server"))
    print()


def example_mcp_http():
    """Example 6: HTTP-based MCP server"""
    print("=" * 60)
    print("Example 6: HTTP MCP Server")
    print("=" * 60)
    
    config = AgentConfig()
    agent = Agent(config=config)
    
    # Register HTTP-based MCP server
    mcp_config = MCPServerConfig(
        name="web-api",
        command="",  # Not needed for HTTP
        transport="http",
        url="http://localhost:8000",  # MCP server URL
        enabled=True
    )
    
    agent.add_mcp_server(mcp_config)
    print(f"HTTP MCP server registered: web-api")
    print()


async def example_mcp_async():
    """Example 7: Async MCP usage"""
    print("=" * 60)
    print("Example 7: Async MCP Operations")
    print("=" * 60)
    
    config = AgentConfig()
    agent = Agent(config=config)
    
    # Register server
    mcp_config = MCPServerConfig(
        name="async-server",
        command="python -m my_mcp_server",
        transport="stdio",
        enabled=True
    )
    agent.add_mcp_server(mcp_config)
    
    # Connect to server (async)
    success = await agent.connect_mcp_server("async-server")
    
    if success:
        print(f"Connected to async-server")
        
        # List available tools
        client = agent.mcp_manager.get_client("async-server")
        if client:
            print(f"Available tools: {list(client.tools.keys())}")
        
        # Disconnect
        await agent.disconnect_mcp_server("async-server")
        print(f"Disconnected from async-server")
    else:
        print(f"Failed to connect to async-server")
    
    print()


def example_status():
    """Example 8: Check agent status"""
    print("=" * 60)
    print("Example 8: Agent Status")
    print("=" * 60)
    
    agent = Agent()
    status = agent.get_status()
    
    for key, value in status.items():
        if isinstance(value, list):
            print(f"{key}: {', '.join(value) if value else '(empty)'}")
        else:
            print(f"{key}: {value}")
    print()


if __name__ == "__main__":
    """Run examples"""
    try:
        # Uncomment the examples you want to run
        
        example_basic_chat()
        # example_agentic_loop()
        # example_custom_config()
        # example_conversation()
        example_mcp_setup()
        example_mcp_http()
        # asyncio.run(example_mcp_async())
        example_status()
        
        print("=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nMake sure you have Ollama running:")
        print("  1. Install Ollama: brew install ollama")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull a model: ollama pull mistral")
