"""NLP Chatbot Engine - A modular NLP engine for building production chatbots."""

__version__ = "0.1.0"

from .core.engine import ChatbotEngine
from .intents.intent_classifier import IntentClassifier
from .entities.entity_extractor import EntityExtractor
from .memory.context_manager import ContextManager

__all__ = [
    "ChatbotEngine",
    "IntentClassifier",
    "EntityExtractor",
    "ContextManager",
]
