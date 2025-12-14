# NLP Chatbot Engine

Production-ready NLP chatbot framework with modular pipelines for building intelligent conversational AI systems.

## 🚀 Features

### Core NLP Capabilities
- **Intent Classification**: Transformer-based intent recognition with rule-based fallback
- **Entity Extraction**: Named entity recognition using spaCy with custom pattern support
- **Dialogue Management**: Context-aware response generation with conversation flow management

### RAG-Ready Architecture
- **Vector Database Integration**: Support for FAISS, ChromaDB, and PGVector
- **Semantic Search**: Retrieve relevant context using sentence transformers
- **Knowledge Base Management**: Easy document ingestion and retrieval

### Multichannel Adapters
- **Web**: Direct web API integration
- **Slack**: Real-time Slack bot integration
- **Microsoft Teams**: Teams bot support with webhooks
- **WhatsApp**: WhatsApp Business API via Twilio

### Memory Management
- **Short-term Memory**: Redis-based session management with TTL
- **Long-term Memory**: SQL database for persistent conversation history
- **Conversation Summarization**: Automatic summarization for long conversations

### Safety & Security
- **Content Safety Filters**: Detect and block inappropriate content
- **Rate Limiting**: Per-user rate limiting with Redis support
- **PII Detection**: Identify and flag personally identifiable information

### Evaluation & Testing
- **Evaluation Harness**: Built-in test suite for intent classification and entity extraction
- **Test Conversations**: Pre-defined conversation flows for testing
- **Metrics Dashboard**: Accuracy and confidence scoring

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **NLP**: Hugging Face Transformers, spaCy, sentence-transformers
- **Vector DB**: FAISS, ChromaDB, PGVector
- **Cache/Queue**: Redis, Celery/RQ
- **Database**: SQLAlchemy (SQLite, PostgreSQL)
- **Deployment**: Docker, uvicorn

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Redis (optional, for memory and rate limiting)
- PostgreSQL (optional, for production database)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/manojsai7/nlp-chatbot-engine
cd nlp-chatbot-engine
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
docker build -t nlp-chatbot-engine .
docker run -p 8000:8000 nlp-chatbot-engine
```

## 🔧 Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

Key configurations:
- `VECTOR_DB_TYPE`: Choose between "faiss", "chroma", or "pgvector"
- `RATE_LIMIT_ENABLED`: Enable/disable rate limiting
- `LONG_TERM_MEMORY_ENABLED`: Enable/disable persistent storage
- `SAFETY_FILTER_ENABLED`: Enable/disable content filtering

## 📚 API Documentation

Once running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

### Core Endpoints

#### Chat
```bash
POST /api/v1/chat
```
Send a message and receive a response with intent and entities.

**Example:**
```json
{
  "message": "Hello, I need help with something",
  "user_id": "user123",
  "session_id": "optional-session-id",
  "channel": "web"
}
```

**Response:**
```json
{
  "response": "I'm here to help! What do you need assistance with?",
  "intent": {
    "name": "help",
    "confidence": 0.85,
    "entities": []
  },
  "entities": [],
  "session_id": "session-uuid",
  "confidence": 0.85,
  "suggestions": ["What specifically do you need help with?"]
}
```

#### Get Conversation History
```bash
GET /api/v1/conversation/{session_id}
```

#### Clear Conversation
```bash
DELETE /api/v1/conversation/{session_id}
```

#### Get User History
```bash
GET /api/v1/user/{user_id}/history?limit=50
```

#### Run Evaluation
```bash
GET /api/v1/evaluate
```

## 🏗️ Architecture

```
nlp-chatbot-engine/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── core/                   # Core models and config
│   │   ├── config.py          # Settings management
│   │   └── models.py          # Pydantic models
│   ├── nlp/                   # NLP modules
│   │   ├── intent_classifier.py
│   │   ├── entity_extractor.py
│   │   └── dialogue_manager.py
│   ├── rag/                   # RAG components
│   │   ├── vector_db.py       # Vector database
│   │   ├── embeddings.py      # Embedding generation
│   │   └── retriever.py       # Document retrieval
│   ├── memory/                # Memory management
│   │   ├── short_term.py      # Redis-based memory
│   │   ├── long_term.py       # Database storage
│   │   └── summarizer.py      # Conversation summarization
│   ├── adapters/              # Channel adapters
│   │   ├── web.py
│   │   ├── slack.py
│   │   ├── teams.py
│   │   └── whatsapp.py
│   ├── middleware/            # Middleware
│   │   ├── safety.py          # Content filtering
│   │   └── rate_limit.py      # Rate limiting
│   └── evaluation/            # Evaluation harness
│       └── harness.py
├── tests/                     # Test suite
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── README.md                  # This file
```

## 🧪 Testing

Run the built-in evaluation harness:
```bash
curl http://localhost:8000/api/v1/evaluate
```

Run tests (if implemented):
```bash
pytest tests/
```

## 🚀 Production Deployment

### Environment Setup
1. Use PostgreSQL for the database
2. Deploy Redis for caching and rate limiting
3. Configure vector database (FAISS for simplicity, PGVector for scale)
4. Set up proper secrets management
5. Enable HTTPS and authentication

### Scaling Considerations
- Use load balancer for multiple API instances
- Separate vector DB for better performance
- Implement message queue (Celery/RQ) for async processing
- Monitor with logging aggregation (ELK, Datadog)

## 🗺️ Roadmap

- [ ] **LLM Integration**: Add LLM-powered intent fallback with OpenAI/Anthropic
- [ ] **Web Admin Panel**: Dashboard for conversation review and analytics
- [ ] **Analytics**: Built-in analytics dashboard with metrics
- [ ] **Multilingual Support**: Multi-language NLP models
- [ ] **Voice Support**: Speech-to-text and text-to-speech
- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Improved RAG**: Better retrieval with re-ranking and hybrid search
- [ ] **Sentiment Analysis**: Real-time sentiment detection
- [ ] **A/B Testing**: Built-in experimentation framework

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI, Hugging Face Transformers, and spaCy
- Inspired by modern conversational AI architectures
- Community contributions and feedback

## 📞 Support

For questions and support, please open an issue on GitHub.

---

**Built with ❤️ for the conversational AI community**
