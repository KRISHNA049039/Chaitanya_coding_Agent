"""
Simple test to see if agent works at all
"""
from agent import Agent
import time

print("Creating agent...")
agent = Agent()

print("Sending simple message...")
start = time.time()

try:
    response = agent.run("Say hello in one word", max_iterations=2, verbose=True)
    elapsed = time.time() - start
    print(f"\n✓ Response received in {elapsed:.1f}s:")
    print(response)
except Exception as e:
    elapsed = time.time() - start
    print(f"\n✗ Error after {elapsed:.1f}s:")
    print(e)
    import traceback
    traceback.print_exc()
