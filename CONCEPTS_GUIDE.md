# 📚 Concepts Guide

## Core Concepts

### 1. Agentic AI

**What is it?**
An AI agent that can reason, plan, and execute actions autonomously using tools.

**How it works:**
```
User: "Create a Python script that fetches weather data"

Agent thinks:
1. I need to create a file
2. I need to write Python code
3. I should use a weather API

Agent actions:
1. Use create_file tool
2. Write code with requests library
3. Return result to user
```

**Key Features:**
- Autonomous decision-making
- Tool selection and execution
- Multi-step reasoning
- Self-correction

### 2. Tool Calling

**What is it?**
The ability for an LLM to invoke external functions/tools.

**Example:**
```python
# Agent decides to use a tool
{
  "action": "use_tool",
  "tool_name": "create_file",
  "arguments": {
    "path": "weather.py",
    "content": "import requests...",
    "reason": "Creating weather script"
  }
}
```

**Tool Types:**
- **Read-only:** web_search, read_file, pdf_info
- **Write:** create_file, modify_file, delete_file
- **Execute:** execute_shell, execute_code
- **Search:** semantic_search, vector_search

### 3. Conversation History

**What is it?**
Maintaining context across multiple messages.

**Structure:**
```python
[
  Message(role="user", content="Hello"),
  Message(role="assistant", content="Hi! How can I help?"),
  Message(role="user", content="Create a file"),
  Message(role="assistant", content="I'll create that...")
]
```

**Benefits:**
- Context awareness
- Follow-up questions
- Reference previous messages
- Coherent conversations

### 4. System Prompt

**What is it?**
Instructions that define the agent's behavior and capabilities.

**Components:**
```
1. Identity: "You are Kiro, an AI coding agent"
2. Capabilities: "You can create files, search web, etc."
3. Rules: "Always explain your actions"
4. Tool descriptions: "create_file: Creates a new file..."
5. Examples: "To create a file, use..."
```

**Why important?**
- Guides agent behavior
- Defines available tools
- Sets expectations
- Improves accuracy

### 5. Approval System

**What is it?**
User confirmation required before executing dangerous operations.

**Flow:**
```
Agent: "I want to delete old_file.txt"
   ↓
System: Create approval request
   ↓
User: Sees modal with details
   ↓
User: Clicks "Approve" or "Reject"
   ↓
System: Execute or cancel
```

**Protected Operations:**
- File creation/modification/deletion
- Shell command execution
- Database modifications

### 6. Streaming Responses

**What is it?**
Sending response tokens as they're generated, not all at once.

**Non-streaming:**
```
User: "Explain Python"
[Wait 30 seconds...]
Agent: "Python is a programming language..."
```

**Streaming:**
```
User: "Explain Python"
Agent: "Python"
Agent: " is"
Agent: " a"
Agent: " programming"
Agent: " language..."
```

**Benefits:**
- Faster perceived response time
- Better UX
- Can cancel mid-response
- Progress indication

### 7. Vector Search

**What is it?**
Semantic search using embeddings instead of keywords.

**Traditional Search:**
```
Query: "machine learning"
Matches: Documents containing "machine" AND "learning"
```

**Vector Search:**
```
Query: "machine learning"
Embedding: [0.2, 0.8, 0.1, ...]
Matches: Documents with similar embeddings
  - "AI and neural networks" (similar concept)
  - "deep learning tutorial" (related topic)
```

**How it works:**
1. Convert text to vector (embedding)
2. Store vectors in database
3. Query with vector
4. Find similar vectors (cosine similarity)
5. Return matching documents

### 8. MCP (Model Context Protocol)

**What is it?**
A standard protocol for connecting AI agents to external tools and data sources.

**Architecture:**
```
┌─────────┐         ┌─────────┐         ┌─────────┐
│  Agent  │ ←─MCP─→ │  Server │ ←─API─→ │ Service │
└─────────┘         └─────────┘         └─────────┘
```

**Benefits:**
- Standardized interface
- Easy integration
- Dynamic tool discovery
- Extensibility

**Example Servers:**
- AWS Docs (documentation search)
- GitHub (repository operations)
- Filesystem (file operations)
- Database (SQL queries)

### 9. Lazy Loading

**What is it?**
Delaying initialization until first use.

**Eager Loading (slow startup):**
```python
def __init__(self):
    self.agent = Agent()  # Takes 30s to load
    print("Ready!")  # User waits 30s
```

**Lazy Loading (fast startup):**
```python
def __init__(self):
    self.agent = None  # Instant
    print("Ready!")  # User sees this immediately

def _ensure_agent(self):
    if self.agent is None:
        self.agent = Agent()  # Load on first use
```

**Benefits:**
- Faster startup
- Better UX
- Resource efficiency
- On-demand loading

### 10. Session Management

**What is it?**
Tracking user interactions across multiple requests.

**Session Data:**
```python
{
  "session_id": "abc123",
  "user_id": 42,
  "started_at": "2026-02-25T10:00:00",
  "conversation_history": [...],
  "pending_approvals": {...}
}
```

**Benefits:**
- Persistent conversations
- User preferences
- Context retention
- Multi-user support

---

## Advanced Concepts

### 11. Agentic Loop

**What is it?**
Iterative process where agent reasons, acts, observes, and repeats.

**Loop Structure:**
```
1. Observe: Read user input
2. Think: Decide what to do
3. Act: Execute tool
4. Observe: See result
5. Think: Is task complete?
   ├─ No → Go to step 3
   └─ Yes → Return response
```

**Example:**
```
User: "Create a Python project with tests"

Iteration 1:
  Think: Need to create main file
  Act: create_file("main.py", ...)
  Observe: File created

Iteration 2:
  Think: Need to create test file
  Act: create_file("test_main.py", ...)
  Observe: File created

Iteration 3:
  Think: Task complete
  Return: "Created Python project with tests"
```

### 12. Context Window

**What is it?**
Maximum amount of text the LLM can process at once.

**Limits:**
- llama3.2:3b → 4096 tokens (~3000 words)
- llama3.1:8b → 8192 tokens (~6000 words)
- GPT-4 → 128k tokens (~96000 words)

**Managing Context:**
```python
# Trim old messages
if len(history) > 10:
    history = history[-10:]  # Keep last 10

# Summarize old context
if len(history) > 20:
    summary = summarize(history[:10])
    history = [summary] + history[10:]
```

### 13. Embeddings

**What is it?**
Converting text into numerical vectors that capture meaning.

**Example:**
```
Text: "Python programming"
Embedding: [0.2, 0.8, 0.1, 0.5, 0.3, ...]
           384 dimensions

Similar texts have similar vectors:
"Python coding" → [0.21, 0.79, 0.12, 0.48, 0.31, ...]
```

**Uses:**
- Semantic search
- Similarity comparison
- Clustering
- Classification

### 14. Prompt Engineering

**What is it?**
Crafting prompts to get better LLM responses.

**Techniques:**

**1. Few-shot Learning:**
```
Examples:
Input: "Create hello.py"
Output: {"action": "use_tool", "tool_name": "create_file", ...}

Input: "Search for Python tutorials"
Output: {"action": "use_tool", "tool_name": "web_search", ...}

Now:
Input: "Make a new file"
Output: ?
```

**2. Chain-of-Thought:**
```
Think step by step:
1. User wants to create a file
2. I need to use create_file tool
3. I need path and content
4. Execute the tool
```

**3. Role Playing:**
```
You are an expert Python developer.
You write clean, efficient code.
You always add docstrings.
```

### 15. Rate Limiting

**What is it?**
Restricting number of requests per time period.

**Implementation:**
```python
# Simple rate limiter
requests_per_minute = 10
last_requests = []

def check_rate_limit():
    now = time.time()
    # Remove old requests
    last_requests = [t for t in last_requests if now - t < 60]
    
    if len(last_requests) >= requests_per_minute:
        raise RateLimitError("Too many requests")
    
    last_requests.append(now)
```

**Why needed?**
- Prevent abuse
- Protect resources
- Fair usage
- Cost control

### 16. Caching

**What is it?**
Storing results to avoid recomputation.

**Types:**

**1. Response Caching:**
```python
cache = {}

def get_response(prompt):
    if prompt in cache:
        return cache[prompt]  # Instant
    
    response = llm.generate(prompt)  # Slow
    cache[prompt] = response
    return response
```

**2. Embedding Caching:**
```python
# Don't recompute embeddings
if doc_id in embedding_cache:
    return embedding_cache[doc_id]
```

**3. System Prompt Caching:**
```python
# Build once, reuse many times
if not self._system_prompt_cache:
    self._system_prompt_cache = self._build_system_prompt()
return self._system_prompt_cache
```

### 17. Error Recovery

**What is it?**
Handling failures gracefully and retrying.

**Strategies:**

**1. Retry with Backoff:**
```python
for attempt in range(3):
    try:
        return llm.generate(prompt)
    except TimeoutError:
        time.sleep(2 ** attempt)  # 1s, 2s, 4s
```

**2. Fallback:**
```python
try:
    return ollama.generate(prompt)
except:
    return openai.generate(prompt)  # Fallback to API
```

**3. Graceful Degradation:**
```python
try:
    return semantic_search(query)
except:
    return keyword_search(query)  # Simpler fallback
```

### 18. Observability

**What is it?**
Understanding system behavior through logs, metrics, and traces.

**Three Pillars:**

**1. Logs:**
```python
logger.info("User request received")
logger.error("LLM timeout", exc_info=True)
```

**2. Metrics:**
```python
response_time.observe(duration)
requests_total.inc()
errors_total.inc()
```

**3. Traces:**
```python
with tracer.span("agent.run"):
    with tracer.span("llm.generate"):
        response = llm.generate(prompt)
```

### 19. A/B Testing

**What is it?**
Comparing two versions to see which performs better.

**Example:**
```python
if user_id % 2 == 0:
    # Version A: Short system prompt
    prompt = "You are a helpful assistant."
else:
    # Version B: Detailed system prompt
    prompt = "You are Kiro, an expert coding agent..."

# Measure which version gets better results
```

**Metrics:**
- Task success rate
- User satisfaction
- Response time
- Tool usage

### 20. Feature Flags

**What is it?**
Toggling features on/off without code changes.

**Implementation:**
```python
flags = {
    "enable_streaming": True,
    "enable_mcp": True,
    "enable_vector_search": False
}

if flags["enable_streaming"]:
    return stream_response()
else:
    return full_response()
```

**Benefits:**
- Safe rollouts
- Easy rollbacks
- A/B testing
- Gradual releases

---

## Best Practices

### 1. Always Validate Input
```python
if not message or len(message) > 10000:
    raise ValueError("Invalid message")
```

### 2. Use Timeouts
```python
response = requests.get(url, timeout=30)
```

### 3. Handle Errors Gracefully
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Error: {e}")
    return fallback_result()
```

### 4. Log Important Events
```python
logger.info(f"User {user_id} created file {path}")
```

### 5. Cache Expensive Operations
```python
@lru_cache(maxsize=100)
def get_embedding(text):
    return model.encode(text)
```

### 6. Use Type Hints
```python
def process_message(message: str, user_id: int) -> str:
    ...
```

### 7. Write Tests
```python
def test_agent_response():
    agent = Agent()
    response = agent.run("Hello")
    assert len(response) > 0
```

### 8. Monitor Performance
```python
start = time.time()
result = expensive_operation()
duration = time.time() - start
logger.info(f"Operation took {duration}s")
```

---

**Understanding these concepts will help you build better AI agents!** 🚀
