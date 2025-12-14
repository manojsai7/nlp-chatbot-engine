"""Tests for IntentClassifier."""
import pytest
from nlp_chatbot_engine.intents.intent_classifier import IntentClassifier


def test_intent_classifier_initialization():
    """Test classifier initializes correctly."""
    classifier = IntentClassifier()
    assert classifier.intents == {}
    assert classifier.default_intent == "unknown"


def test_add_intent():
    """Test adding intents."""
    classifier = IntentClassifier()
    classifier.add_intent("greeting", keywords=["hello", "hi"])
    
    assert "greeting" in classifier.intents
    assert "hello" in classifier.keywords["greeting"]


def test_add_intent_with_patterns():
    """Test adding intents with patterns."""
    classifier = IntentClassifier()
    classifier.add_intent("test", patterns=[r"^test.*"])
    
    assert "test" in classifier.intents
    assert len(classifier.patterns["test"]) == 1


def test_classify_with_keywords():
    """Test classification with keywords."""
    classifier = IntentClassifier()
    classifier.add_intent("greeting", keywords=["hello", "hi"])
    
    result = classifier.classify("hello there")
    assert result["intent"] == "greeting"
    assert result["confidence"] > 0


def test_classify_with_pattern():
    """Test classification with patterns."""
    classifier = IntentClassifier()
    classifier.add_intent("order", patterns=[r"order.*pizza"])
    
    result = classifier.classify("I want to order a pizza")
    assert result["intent"] == "order"


def test_classify_unknown():
    """Test classification of unknown intent."""
    classifier = IntentClassifier()
    classifier.add_intent("greeting", keywords=["hello"])
    
    result = classifier.classify("random text")
    assert result["intent"] == "unknown"
    assert result["confidence"] == 0.0


def test_train():
    """Test training the classifier."""
    classifier = IntentClassifier()
    
    training_data = [
        {"text": "hello world", "intent": "greeting"},
        {"text": "goodbye friend", "intent": "farewell"},
    ]
    
    classifier.train(training_data)
    
    assert "greeting" in classifier.intents
    assert "farewell" in classifier.intents
    assert classifier.trained is True


def test_classify_with_context():
    """Test classification with context."""
    classifier = IntentClassifier()
    classifier.add_intent("greeting", keywords=["hello"])
    classifier.add_intent("followup", keywords=["yes"])
    
    # First message
    result1 = classifier.classify("hello")
    assert result1["intent"] == "greeting"
    
    # Context boosts last intent
    context = {"last_intent": "greeting"}
    result2 = classifier.classify("hello", context)
    assert result2["intent"] == "greeting"


def test_get_intents():
    """Test getting list of intents."""
    classifier = IntentClassifier()
    classifier.add_intent("intent1")
    classifier.add_intent("intent2")
    
    intents = classifier.get_intents()
    assert "intent1" in intents
    assert "intent2" in intents
    assert len(intents) == 2
