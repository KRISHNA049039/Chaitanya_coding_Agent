"""
Quick test to verify tool parameter names
"""
from agent import Agent

# Create agent
agent = Agent()

# Print tool schemas
print("Available Tools and Their Parameters:\n")
print("="*60)

for name, tool in agent.tools.tools.items():
    schema = tool.schema()
    print(f"\nTool: {name}")
    print(f"Description: {schema.get('description', 'N/A')}")
    if 'parameters' in schema:
        print("Parameters:")
        for param_name, param_desc in schema['parameters'].items():
            print(f"  - {param_name}: {param_desc}")
    print("-"*60)

print("\n\nExample Tool Calls:\n")
print("="*60)

examples = [
    {
        "tool": "create_file",
        "call": {
            "action": "use_tool",
            "tool_name": "create_file",
            "arguments": {
                "path": "example.py",
                "content": "print('Hello, World!')",
                "reason": "Create example script"
            }
        }
    },
    {
        "tool": "read_file",
        "call": {
            "action": "use_tool",
            "tool_name": "read_file",
            "arguments": {
                "path": "config.py"
            }
        }
    },
    {
        "tool": "list_directory",
        "call": {
            "action": "use_tool",
            "tool_name": "list_directory",
            "arguments": {
                "path": ".",
                "recursive": False
            }
        }
    }
]

import json
for example in examples:
    print(f"\n{example['tool']}:")
    print(json.dumps(example['call'], indent=2))
    print("-"*60)
