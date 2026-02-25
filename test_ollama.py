"""
Quick test to check if Ollama is working
"""
import requests

print("Testing Ollama connection...")
print("="*60)

try:
    # Test 1: Check if Ollama is running
    print("\n1. Checking if Ollama is running...")
    response = requests.get('http://localhost:11434/api/tags', timeout=5)
    print(f"   ✓ Ollama is running (status: {response.status_code})")
    
    # Test 2: List available models
    print("\n2. Available models:")
    data = response.json()
    models = data.get('models', [])
    if models:
        for model in models:
            print(f"   - {model.get('name')}")
    else:
        print("   ⚠️  No models found. Run: ollama pull mistral")
    
    # Test 3: Try a simple chat
    print("\n3. Testing chat endpoint...")
    chat_response = requests.post(
        'http://localhost:11434/api/chat',
        json={
            'model': 'llama3.1:8b',
            'messages': [{'role': 'user', 'content': 'Say hello in one word'}],
            'stream': False
        },
        timeout=30
    )
    
    if chat_response.status_code == 200:
        result = chat_response.json()
        reply = result.get('message', {}).get('content', '')
        print(f"   ✓ Chat working! Response: {reply}")
    else:
        print(f"   ✗ Chat failed with status: {chat_response.status_code}")
        print(f"   Response: {chat_response.text}")

except requests.exceptions.ConnectionError:
    print("   ✗ Cannot connect to Ollama")
    print("\n   Solution:")
    print("   1. Start Ollama: ollama serve")
    print("   2. Or check if it's running on a different port")

except requests.exceptions.Timeout:
    print("   ✗ Request timed out")
    print("\n   Solution:")
    print("   1. Ollama might be slow to respond")
    print("   2. Try a smaller model: ollama pull llama3.2:3b")

except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("\nIf all tests pass, your agent should work!")
print("If not, follow the solutions above.\n")
