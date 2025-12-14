# Quick Start Guide

This guide will help you get started with the NLP Chatbot Engine.

## 🚀 Quick Start (3 minutes)

### 1. Clone and Setup
```bash
git clone https://github.com/manojsai7/nlp-chatbot-engine
cd nlp-chatbot-engine
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure (Optional)
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## 📝 Basic Usage

### Simple Chat Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need help!",
    "user_id": "user123",
    "channel": "web"
  }'
```

Response:
```json
{
  "response": "I'm here to help! What do you need assistance with?",
  "intent": {
    "name": "help",
    "confidence": 0.85
  },
  "session_id": "uuid-here",
  "suggestions": ["What specifically do you need help with?"]
}
```

### Get Conversation History

```bash
curl "http://localhost:8000/api/v1/conversation/{session_id}"
```

### Run Evaluation

```bash
curl "http://localhost:8000/api/v1/evaluate"
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

This starts:
- Chatbot API on port 8000
- Redis on port 6379

### Using Docker Only
```bash
docker build -t nlp-chatbot .
docker run -p 8000:8000 nlp-chatbot
```

## 🔧 Configuration Options

Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `VECTOR_DB_TYPE` | `faiss` | Vector database type (faiss/chroma/pgvector) |
| `RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |
| `SAFETY_FILTER_ENABLED` | `true` | Enable content filtering |
| `LONG_TERM_MEMORY_ENABLED` | `true` | Enable persistent storage |
| `REDIS_HOST` | `localhost` | Redis host for caching |
| `DATABASE_URL` | `sqlite:///./chatbot.db` | Database connection string |

See `.env.example` for all options.

## 📊 Features Overview

### 1. Intent Classification
Automatically detects user intent:
- greeting, farewell, question, help, complaint, request, etc.
- Uses transformer models with rule-based fallback

### 2. Entity Extraction
Extracts entities from text:
- Names, locations, organizations (via spaCy)
- Emails, phone numbers (via regex)
- Custom entity patterns

### 3. RAG (Retrieval Augmented Generation)
Add knowledge base documents:
```python
from app.rag.retriever import get_retriever

retriever = get_retriever()
retriever.add_knowledge_base(
    documents=["Document 1", "Document 2"],
    metadata=[{"source": "manual"}, {"source": "faq"}]
)

# Search for relevant documents
results = retriever.retrieve("How do I reset my password?", top_k=3)
```

### 4. Memory Management
- **Short-term**: Session-based (Redis)
- **Long-term**: Persistent (SQLite/PostgreSQL)
- **Summarization**: Auto-compress long conversations

### 5. Multichannel Support
Built-in adapters for:
- Web (direct API)
- Slack
- Microsoft Teams
- WhatsApp (via Twilio)

### 6. Safety & Security
- Content filtering
- PII detection
- Rate limiting (per-user)
- Input validation

## 🧪 Testing

### Run Validation
```bash
python validate_structure.py
```

### Run Examples
```bash
python examples.py
```

### Run Tests (when ML dependencies installed)
```bash
pytest tests/ -v
```

## 🏗️ Architecture

```
Request → Rate Limit → Safety Filter → NLP Pipeline → Dialogue Manager → Response
                                          ↓
                                     Memory Layer
                                     (Short/Long Term)
                                          ↓
                                     RAG Retriever
                                     (Optional)
```

## 📦 Module Structure

- **app/core**: Configuration and models
- **app/nlp**: NLP pipeline (intent, entities, dialogue)
- **app/rag**: RAG components (vector DB, embeddings, retrieval)
- **app/memory**: Memory management (short-term, long-term, summarization)
- **app/adapters**: Channel adapters (web, Slack, Teams, WhatsApp)
- **app/middleware**: Safety filters and rate limiting
- **app/evaluation**: Evaluation harness and metrics

## 🔌 Integration Examples

### Python Client
```python
import httpx

async def chat(message: str, user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/chat",
            json={
                "message": message,
                "user_id": user_id,
                "channel": "web"
            }
        )
        return response.json()

# Usage
result = await chat("Hello!", "user123")
print(result["response"])
```

### JavaScript Client
```javascript
async function chat(message, userId) {
  const response = await fetch('http://localhost:8000/api/v1/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      user_id: userId,
      channel: 'web'
    })
  });
  return await response.json();
}

// Usage
const result = await chat("Hello!", "user123");
console.log(result.response);
```

## 🚨 Troubleshooting

### Issue: Import errors for torch/spacy
**Solution**: Install all requirements
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Issue: Redis connection failed
**Solution**: Redis is optional. Disable in `.env`:
```
RATE_LIMIT_ENABLED=false
```
Or install Redis:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

### Issue: Port 8000 already in use
**Solution**: Use a different port:
```bash
uvicorn app.main:app --port 8080
```

## 📚 Additional Resources

- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **GitHub**: https://github.com/manojsai7/nlp-chatbot-engine
- **Issues**: https://github.com/manojsai7/nlp-chatbot-engine/issues

## 🤝 Contributing

Contributions welcome! See README.md for guidelines.

## 📄 License

MIT License - See LICENSE file for details.
