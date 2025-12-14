"""Tests for intent classifier"""
import pytest
from app.nlp.intent_classifier import IntentClassifier


def test_intent_classifier_initialization():
    """Test intent classifier can be initialized"""
    classifier = IntentClassifier()
    assert classifier is not None


def test_rule_based_greeting():
    """Test rule-based greeting classification"""
    classifier = IntentClassifier()
    intent, confidence = classifier.classify("Hello there!")
    assert intent == "greeting"
    assert confidence > 0.5


def test_rule_based_farewell():
    """Test rule-based farewell classification"""
    classifier = IntentClassifier()
    intent, confidence = classifier.classify("Goodbye!")
    assert intent == "farewell"
    assert confidence > 0.5


def test_rule_based_question():
    """Test rule-based question classification"""
    classifier = IntentClassifier()
    intent, confidence = classifier.classify("What is the weather?")
    assert intent == "question"
    assert confidence > 0.5


def test_rule_based_help():
    """Test rule-based help classification"""
    classifier = IntentClassifier()
    intent, confidence = classifier.classify("I need help")
    assert intent == "help"
    assert confidence > 0.5


def test_batch_classify():
    """Test batch classification"""
    classifier = IntentClassifier()
    texts = ["Hello", "Goodbye", "What time is it?"]
    results = classifier.batch_classify(texts)
    assert len(results) == 3
    assert all(isinstance(r, tuple) for r in results)
