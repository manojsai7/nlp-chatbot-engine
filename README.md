# NLP Chatbot Engine

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
