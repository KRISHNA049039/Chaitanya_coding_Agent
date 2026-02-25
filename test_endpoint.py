import requests
import json

# Test /api/chat endpoint
print("Testing /api/chat...")
try:
    response = requests.post(
        'http://localhost:11434/api/chat',
        json={
            'model': 'llama3.1:8b',
            'messages': [{'role': 'user', 'content': 'hi'}],
            'stream': False
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ /api/chat works!")
        print(response.json())
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test /api/generate endpoint
print("\nTesting /api/generate...")
try:
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'llama3.1:8b',
            'prompt': 'hi',
            'stream': False
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ /api/generate works!")
        print(response.json())
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Failed: {e}")
