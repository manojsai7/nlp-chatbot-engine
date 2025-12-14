"""Tests for the ChatbotEngine core."""
import pytest
from nlp_chatbot_engine import ChatbotEngine, IntentClassifier, EntityExtractor, ContextManager


def test_engine_initialization():
    """Test engine initializes correctly."""
    engine = ChatbotEngine()
    assert engine.intent_classifier is not None
    assert engine.entity_extractor is not None
    assert engine.context_manager is not None


def test_engine_with_custom_components():
    """Test engine with custom components."""
    classifier = IntentClassifier()
    extractor = EntityExtractor()
    context = ContextManager()
    
    engine = ChatbotEngine(
        intent_classifier=classifier,
        entity_extractor=extractor,
        context_manager=context
    )
    
    assert engine.intent_classifier is classifier
    assert engine.entity_extractor is extractor
    assert engine.context_manager is context


def test_register_intent_handler():
    """Test registering intent handlers."""
    engine = ChatbotEngine()
    
    def test_handler(message, entities, context):
        return "Test response"
    
    engine.register_intent_handler("test_intent", test_handler)
    assert "test_intent" in engine._handlers


def test_process_message():
    """Test message processing."""
    engine = ChatbotEngine()
    engine.intent_classifier.add_intent("greeting", keywords=["hello"])
    
    result = engine.process_message("hello", "user1")
    
    assert "intent" in result
    assert "confidence" in result
    assert "entities" in result
    assert result["message"] == "hello"


def test_process_message_with_handler():
    """Test message processing with handler."""
    engine = ChatbotEngine()
    engine.intent_classifier.add_intent("test", keywords=["test"])
    
    def handler(message, entities, context):
        return "Handler response"
    
    engine.register_intent_handler("test", handler)
    
    result = engine.process_message("test message", "user1")
    assert "response" in result
    assert result["response"] == "Handler response"


def test_train_intents():
    """Test intent training."""
    engine = ChatbotEngine()
    
    training_data = [
        {"text": "hello there", "intent": "greeting"},
        {"text": "hi everyone", "intent": "greeting"},
    ]
    
    engine.train_intents(training_data)
    result = engine.process_message("hello", "user1")
    
    assert result["intent"] == "greeting"


def test_add_entity_pattern():
    """Test adding entity patterns."""
    engine = ChatbotEngine()
    engine.add_entity_pattern("custom", r"\btest\b")
    
    result = engine.process_message("this is a test", "user1")
    
    entities = [e for e in result["entities"] if e["type"] == "custom"]
    assert len(entities) > 0


def test_clear_context():
    """Test clearing user context."""
    engine = ChatbotEngine()
    
    engine.process_message("test", "user1")
    assert engine.context_manager.has_context("user1")
    
    engine.clear_context("user1")
    assert not engine.context_manager.has_context("user1")
