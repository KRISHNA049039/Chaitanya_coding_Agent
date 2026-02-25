"""
Test approval callback
"""
from agent import Agent
from file_operations import FileChange

print("Creating agent...")
agent = Agent()

print("Setting up callback...")
callback_triggered = False

def test_callback(change_id, change):
    global callback_triggered
    callback_triggered = True
    print(f"✓ Callback triggered! change_id={change_id}, path={change.path}")

agent.approval_handler.set_approval_callback(test_callback)

print("Testing create_file tool...")
result = agent.tools.execute(
    "create_file",
    path="test_approval.txt",
    content="Hello World",
    reason="Testing approval"
)

print(f"\nTool result: {result.output}")
print(f"Callback triggered: {callback_triggered}")

if callback_triggered:
    print("\n✓ SUCCESS: Approval callback is working!")
else:
    print("\n✗ FAILED: Approval callback was not triggered")
