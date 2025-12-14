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
=======
A modular NLP engine for building production chatbots with intents, entities, memory, and multi-channel connectors.

## Features

- **Intent Classification**: Identify user intentions using keyword and pattern matching
- **Entity Extraction**: Extract structured information (emails, phones, URLs, numbers, dates, custom entities)
- **Context Management**: Maintain conversation state and memory across messages
- **Multi-Channel Connectors**: Support for Web, Slack, Discord, and custom channels
- **Modular Architecture**: Easy to extend and customize for your needs
- **Production Ready**: Built with scalability and reliability in mind

## Installation

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -e .
```

## Quick Start

```python
from nlp_chatbot_engine import ChatbotEngine

# Initialize the engine
engine = ChatbotEngine()

# Configure intents
engine.intent_classifier.add_intent(
    "greeting",
    keywords=["hello", "hi", "hey"],
    patterns=[r"^(hello|hi)"]
)

# Register intent handler
def handle_greeting(message, entities, context):
    return "Hello! How can I help you?"

engine.register_intent_handler("greeting", handle_greeting)

# Process a message
result = engine.process_message("Hello there!", user_id="user123")
print(result["response"])  # "Hello! How can I help you?"
```

## Core Components

### 1. ChatbotEngine

The main orchestrator that integrates all components:

```python
from nlp_chatbot_engine import ChatbotEngine

engine = ChatbotEngine()

# Process messages
result = engine.process_message(
    message="I want to order a pizza",
    user_id="user123"
)
```

### 2. Intent Classification

Identify what users want to do:

```python
# Add intents with keywords
engine.intent_classifier.add_intent(
    "order_pizza",
    keywords=["pizza", "order", "delivery"],
    patterns=[r"(order|want|get).*pizza"]
)

# Train with examples
training_data = [
    {"text": "I want pizza", "intent": "order_pizza"},
    {"text": "Order a large pizza", "intent": "order_pizza"}
]
engine.train_intents(training_data)
```

### 3. Entity Extraction

Extract structured information from text:

```python
# Built-in entity types: email, phone, url, number, date
result = engine.process_message(
    "Contact me at john@example.com or 555-1234",
    user_id="user123"
)
# Entities: [{"type": "email", "value": "john@example.com"}, 
#            {"type": "phone", "value": "555-1234"}]

# Add custom entity patterns
engine.add_entity_pattern("product_code", r"PROD-\d{4}")

# Add custom extractors
def extract_cities(text):
    cities = ["New York", "London", "Paris"]
    return [{"value": city} for city in cities if city in text]

engine.entity_extractor.add_custom_extractor("city", extract_cities)
```

### 4. Context Management

Maintain conversation state:

```python
# Context is automatically managed
result1 = engine.process_message("Book a hotel in Paris", "user123")
result2 = engine.process_message("Yes, confirm", "user123")

# Access context manually
context = engine.context_manager.get_context("user123")

# Clear context when done
engine.clear_context("user123")
```

### 5. Multi-Channel Connectors

Connect to different platforms:

#### Web/REST API
```python
from nlp_chatbot_engine.connectors.web_connector import WebConnector

connector = WebConnector(engine)
connector.connect()

response = connector.handle_request("user123", "Hello")
print(response["response"])
```

#### Slack
```python
from nlp_chatbot_engine.connectors.slack_connector import SlackConnector

config = {"bot_token": "xoxb-your-token"}
connector = SlackConnector(engine, config)
connector.connect()

# Handle Slack events
connector.handle_event(slack_event_data)
```

#### Discord
```python
from nlp_chatbot_engine.connectors.discord_connector import DiscordConnector

config = {"bot_token": "your-discord-token"}
connector = DiscordConnector(engine, config)
connector.connect()

# Handle Discord messages
connector.handle_message_event(discord_message)
```

## Examples

See the `examples/` directory for complete examples:

- `basic_usage.py` - Basic chatbot setup
- `connector_example.py` - Multi-channel connector usage
- `context_example.py` - Context and memory management

Run examples:
```bash
python examples/basic_usage.py
python examples/connector_example.py
python examples/context_example.py
```

## Testing

Run tests with pytest:


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
=======
Run with coverage:
```bash
pytest --cov=nlp_chatbot_engine tests/
```

## Architecture

```
nlp_chatbot_engine/
├── core/
│   └── engine.py          # Main ChatbotEngine
├── intents/
│   └── intent_classifier.py  # Intent classification
├── entities/
│   └── entity_extractor.py   # Entity extraction
├── memory/
│   └── context_manager.py    # Context management
└── connectors/
    ├── base_connector.py      # Base connector interface
    ├── web_connector.py       # Web/REST connector
    ├── slack_connector.py     # Slack connector
    └── discord_connector.py   # Discord connector
```

## Advanced Usage

### Custom Intent Handlers

```python
def handle_order(message, entities, context):
    # Extract order details
    items = [e["value"] for e in entities if e["type"] == "item"]
    
    # Use context
    if "user_location" in context:
        location = context["user_location"]
    
    # Return response
    return f"Order placed for {items} at {location}"

engine.register_intent_handler("place_order", handle_order)
```

### Context Timeout

```python
from nlp_chatbot_engine.memory.context_manager import ContextManager

# Context expires after 1 hour (3600 seconds)
context_manager = ContextManager(context_timeout=3600)
engine = ChatbotEngine(context_manager=context_manager)
```

### Custom Connectors

```python
from nlp_chatbot_engine.connectors.base_connector import BaseConnector

class CustomConnector(BaseConnector):
    def connect(self):
        # Implement connection logic
        self.connected = True
    
    def disconnect(self):
        self.connected = False
    
    def send_message(self, user_id, message, **kwargs):
        # Implement message sending
        pass
    
    def receive_message(self):
        # Implement message receiving
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - See LICENSE file for details

## Author

Manoj Sai

## Links

- GitHub: https://github.com/manojsai7/nlp-chatbot-engine
- Documentation: Coming soon
- Issues: https://github.com/manojsai7/nlp-chatbot-engine/issues

