# 🏗️ Kiro Agent - Complete Architecture

## System Overview

Kiro Agent is a multi-interface AI coding assistant with tool execution, file operations, web search, PDF processing, and MCP integration capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Web UI     │   CLI Chat   │  VS Code Ext │  MCP Server    │
│ (Flask/HTML) │  (Terminal)  │  (TypeScript)│  (stdio/JSON)  │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │              │              │                │
       └──────────────┴──────────────┴────────────────┘
                            │
                    ┌───────▼────────┐
                    │  Agent Core    │
                    │  (agent.py)    │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │   LLM   │        │  Tools  │        │   MCP   │
   │ Client  │        │Registry │        │ Manager │
   └────┬────┘        └────┬────┘        └────┬────┘
        │                  │                   │
   ┌────▼────┐        ┌────▼────────────┐     │
   │ Ollama  │        │ File Operations │     │
   │ (Local) │        │ Shell Commands  │     │
   └─────────┘        │ Web Search      │     │
                      │ PDF Processing  │     │
                      │ Vector Search   │     │
                      │ Semantic Search │     │
                      └─────────────────┘     │
                                              │
                      ┌───────────────────────▼──────┐
                      │  External MCP Servers        │
                      │  - AWS Docs                  │
                      │  - GitHub                    │
                      │  - Custom Servers            │
                      └──────────────────────────────┘
```

## Core Components

### 1. Agent Core (`agent.py`)

**Purpose:** Central orchestration and reasoning engine

**Key Features:**
- Agentic loop with tool calling
- Conversation history management
- System prompt building
- Tool call parsing
- Iteration control

**Flow:**
```python
User Input → Agent → LLM → Parse Response → Tool Call? 
                                              ↓ Yes
                                         Execute Tool
                                              ↓
                                         Add Result
                                              ↓
                                         Loop Back
                                              ↓ No
                                         Return Response
```

### 2. LLM Client (`llm_client.py`)

**Purpose:** Interface to local LLM (Ollama)

**Features:**
- Chat completion API
- Streaming support
- Timeout handling
- Error recovery

**Supported Models:**
- llama3.2:3b (fast)
- llama3.1:8b (balanced)
- mistral:7b (quality)
- gemma2:2b (fastest)

### 3. Tool Registry (`tools.py`)

**Purpose:** Plugin system for agent capabilities

**Built-in Tools:**
- `create_file` - Create new files (requires approval)
- `modify_file` - Modify existing files (requires approval)
- `delete_file` - Delete files (requires approval)
- `list_directory` - List directory contents
- `execute_shell` - Run shell commands (requires approval)
- `read_file` - Read file contents
- `web_search` - Search the internet
- `fetch_url` - Fetch webpage content
- `quick_answer` - Get quick answers
- `read_pdf` - Extract text from PDFs
- `pdf_info` - Get PDF metadata
- `search_pdf` - Search within PDFs
- `find_pdfs` - Find PDF files
- `semantic_search` - Vector-based search
- `code_search` - Search code semantically

### 4. File Operations (`file_operations.py`)

**Purpose:** Safe file manipulation with user approval

**Approval Flow:**
```
Agent proposes change → Create FileChange object → Request approval
                                                          ↓
                                                    User approves?
                                                          ↓ Yes
                                                    Execute change
                                                          ↓
                                                    Return result
```

**Security:**
- Path normalization (prevents `/` absolute paths)
- Directory traversal prevention
- Approval required for all modifications

### 5. MCP Integration (`mcp_client.py`)

**Purpose:** Connect to external Model Context Protocol servers

**Capabilities:**
- Dynamic tool discovery
- Async communication
- Server lifecycle management
- Tool registration

**Supported Transports:**
- stdio (standard input/output)
- HTTP (future)
- WebSocket (future)

### 6. Database (`database.py`)

**Purpose:** Persistent storage for conversations and context

**Schema:**
```sql
users
  - id, username, email, preferences, created_at

sessions
  - id, user_id, started_at, last_active, session_metadata

messages
  - id, session_id, role, content, tokens_used, tool_calls, created_at

context_store
  - id, user_id, key, value, created_at, updated_at
```

### 7. Vector Search (`vector_search.py`)

**Purpose:** Semantic search over documents and code

**Features:**
- Sentence transformers (all-MiniLM-L6-v2)
- In-memory vector store
- Cosine similarity search
- Document chunking

## User Interfaces

### 1. Web UI (`web_ui.py`)

**Technology:** Flask + HTML/CSS/JavaScript

**Features:**
- Chat interface
- Approval modals
- Session management
- Multi-user support

**Endpoints:**
- `GET /` - Main chat page
- `POST /api/chat` - Send message
- `POST /api/approve` - Approve change
- `POST /api/reject` - Reject change
- `GET /api/health` - Health check

### 2. CLI Chat (`cli_chat.py`)

**Technology:** Python + colorama

**Features:**
- Streaming responses
- Inline approvals
- Color-coded output
- Command system

**Commands:**
- `/help` - Show help
- `/clear` - Clear history
- `/tools` - List tools
- `/exit` - Exit
- `approve <id>` - Approve change
- `reject <id>` - Reject change

### 3. VS Code Extension (`vscode-extension/`)

**Technology:** TypeScript + VS Code API

**Features:**
- Sidebar panel
- Streaming chat
- Inline approval buttons
- IDE integration

**Components:**
- `extension.ts` - Main extension logic
- `package.json` - Extension manifest
- Webview UI with SSE streaming

### 4. MCP Server (`mcp_server_wrapper.py`)

**Technology:** Python + JSON-RPC

**Features:**
- stdio transport
- Lazy agent loading
- UTF-8 encoding
- Error handling

**Tools Exposed:**
- `chat` - Chat with agent
- `get_status` - Get agent status

## Data Flow

### Chat Request Flow

```
1. User sends message
   ↓
2. Interface receives input
   ↓
3. Agent.run() called
   ↓
4. Build system prompt with tools
   ↓
5. Send to LLM
   ↓
6. Parse LLM response
   ↓
7. Tool call detected?
   ├─ Yes → Execute tool → Add result → Loop to step 5
   └─ No → Return response
   ↓
8. Display to user
```

### File Operation Flow

```
1. Agent decides to create/modify file
   ↓
2. Create FileChange object
   ↓
3. Request approval via callback
   ↓
4. Store in pending_approvals dict
   ↓
5. Send approval request to UI
   ↓
6. User clicks Approve/Reject
   ↓
7. Execute or discard change
   ↓
8. Return result to agent
```

### MCP Tool Flow

```
1. Agent initialized
   ↓
2. Connect to MCP servers
   ↓
3. Discover available tools
   ↓
4. Register tools in registry
   ↓
5. Agent can now use MCP tools
   ↓
6. Tool call → MCP client → Server → Result
```

## Configuration

### Environment Variables (`.env`)

```env
# LLM Configuration
LLM_MODEL_NAME=llama3.2:3b
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
LLM_TIMEOUT=180

# Agent Configuration
DEBUG=False
ENABLE_MCP=True

# Database
DATABASE_URL=sqlite:///kiro_agent.db
```

### MCP Configuration (`mcp.json`)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Security Considerations

### 1. File Operations
- ✅ Path normalization
- ✅ User approval required
- ✅ Directory traversal prevention
- ✅ Relative paths enforced

### 2. Shell Commands
- ✅ User approval required
- ✅ Timeout limits
- ✅ Output sanitization
- ⚠️ No command validation (trust user approval)

### 3. Web Search
- ✅ No approval needed (read-only)
- ✅ Rate limiting (external)
- ✅ Content sanitization

### 4. Database
- ✅ SQLAlchemy ORM (SQL injection protection)
- ✅ Session isolation
- ⚠️ No encryption at rest

### 5. MCP Servers
- ⚠️ Trust external servers
- ✅ Timeout protection
- ✅ Error isolation

## Performance Characteristics

### Response Times (CPU)

| Operation | Time | Notes |
|-----------|------|-------|
| Simple chat | 30-60s | llama3.2:3b |
| Tool execution | +5-10s | Per tool |
| File read | <1s | Small files |
| Web search | 2-5s | Network dependent |
| PDF read | 1-5s | Per 10 pages |
| Vector search | <1s | In-memory |

### Response Times (GPU - Intel Arc)

| Operation | Time | Notes |
|-----------|------|-------|
| Simple chat | 5-10s | 20-30 tok/s |
| Tool execution | +5-10s | Per tool |

### Memory Usage

| Component | Memory | Notes |
|-----------|--------|-------|
| Agent core | ~100MB | Base |
| LLM model | 2-5GB | Model dependent |
| Vector store | ~50MB | Per 1000 docs |
| Web UI | ~50MB | Flask |
| Database | ~10MB | SQLite |

### Scalability

**Current Limits:**
- Single process
- In-memory vector store
- SQLite database
- Local LLM only

**Scaling Options:**
- Multi-process (Gunicorn)
- Redis for vector store
- PostgreSQL database
- Remote LLM API

## Dependencies

### Core
- `ollama` - LLM client
- `pydantic` - Data validation
- `python-dotenv` - Environment config

### Web
- `flask` - Web framework
- `flask-cors` - CORS support
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing

### Database
- `sqlalchemy` - ORM
- `sqlite3` - Database (built-in)

### AI/ML
- `sentence-transformers` - Embeddings
- `PyPDF2` - PDF processing

### UI
- `colorama` - Terminal colors
- `typer` - CLI framework

### Development
- `typescript` - VS Code extension
- `@types/vscode` - VS Code types

## Deployment Options

### 1. Local Development
```bash
python web_ui.py
# or
python cli_chat.py
```

### 2. Docker Container
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "web_ui.py"]
```

### 3. Production Server
```bash
gunicorn -w 4 -b 0.0.0.0:5000 web_ui:app
```

### 4. VS Code Extension
```bash
cd vscode-extension
npm run package
code --install-extension kiro-agent-0.1.0.vsix
```

### 5. MCP Server
```json
{
  "mcpServers": {
    "my-agent": {
      "command": "python",
      "args": ["mcp_server_wrapper.py"]
    }
  }
}
```

## Monitoring & Debugging

### Logs

**Web UI:**
```python
print(f"[DEBUG] Message: {message}")
```

**CLI:**
```python
logger.info("Agent initialized")
```

**MCP Server:**
```python
# Logs to stderr
logger.error("Error", exc_info=True)
```

### Health Checks

**Web UI:**
```bash
curl http://localhost:5000/api/health
```

**LLM:**
```bash
ollama ps
```

**Database:**
```python
from database import db_manager
db_manager.get_session()
```

### Performance Monitoring

**LLM Stats:**
```bash
ollama ps  # Check token rate
```

**Memory:**
```bash
# Windows
tasklist | findstr python

# Linux
ps aux | grep python
```

## Testing

### Unit Tests
```python
# test_agent.py
def test_agent_initialization():
    agent = Agent()
    assert agent.llm is not None
```

### Integration Tests
```python
# test_tools.py
def test_file_creation():
    tool = CreateFileTool(approval_handler)
    result = tool.execute(path="test.txt", content="hello")
    assert result.success
```

### End-to-End Tests
```bash
# Test web UI
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Troubleshooting

### Common Issues

**1. LLM Timeout**
- Increase `LLM_TIMEOUT`
- Use smaller model
- Enable GPU

**2. MCP Connection Failed**
- Check server path
- Verify Python environment
- Check logs in stderr

**3. File Permission Denied**
- Check file paths
- Verify write permissions
- Use relative paths

**4. Unicode Errors**
- Set `PYTHONIOENCODING=utf-8`
- Remove emoji characters
- Use ASCII-safe encoding

**5. Database Locked**
- Close other connections
- Use PostgreSQL for multi-user
- Check file permissions

## Future Enhancements

See `PRODUCTION_ROADMAP.md` for detailed production plan.

---

**Architecture Version:** 1.0  
**Last Updated:** 2026-02-25  
**Maintainer:** Chaitanya
