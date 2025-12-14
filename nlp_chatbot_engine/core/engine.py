"""Main chatbot engine implementation."""
from typing import Dict, Any, Optional, List
from ..intents.intent_classifier import IntentClassifier
from ..entities.entity_extractor import EntityExtractor
from ..memory.context_manager import ContextManager


class ChatbotEngine:
    """
    Main chatbot engine that orchestrates NLP processing.
    
    This class integrates intent classification, entity extraction,
    and context management to process user messages.
    """
    
    def __init__(
        self,
        intent_classifier: Optional[IntentClassifier] = None,
        entity_extractor: Optional[EntityExtractor] = None,
        context_manager: Optional[ContextManager] = None,
    ):
        """
        Initialize the chatbot engine.
        
        Args:
            intent_classifier: Intent classification module
            entity_extractor: Entity extraction module
            context_manager: Context/memory management module
        """
        self.intent_classifier = intent_classifier or IntentClassifier()
        self.entity_extractor = entity_extractor or EntityExtractor()
        self.context_manager = context_manager or ContextManager()
        self._handlers = {}
    
    def register_intent_handler(self, intent: str, handler: callable):
        """
        Register a handler function for a specific intent.
        
        Args:
            intent: Intent name
            handler: Callable that processes the intent
        """
        self._handlers[intent] = handler
    
    def process_message(
        self,
        message: str,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the NLP pipeline.
        
        Args:
            message: User's input message
            user_id: Unique identifier for the user
            metadata: Additional metadata about the message
        
        Returns:
            Dictionary containing processing results
        """
        # Get user context
        context = self.context_manager.get_context(user_id)
        
        # Classify intent
        intent_result = self.intent_classifier.classify(message, context)
        
        # Extract entities
        entities = self.entity_extractor.extract(message, intent_result.get("intent"))
        
        # Update context
        self.context_manager.update_context(
            user_id,
            {
                "last_message": message,
                "last_intent": intent_result.get("intent"),
                "entities": entities,
            }
        )
        
        # Prepare response
        result = {
            "message": message,
            "intent": intent_result.get("intent"),
            "confidence": intent_result.get("confidence"),
            "entities": entities,
            "context": context,
        }
        
        # Execute handler if registered
        if intent_result.get("intent") in self._handlers:
            handler_result = self._handlers[intent_result.get("intent")](
                message, entities, context
            )
            result["response"] = handler_result
        
        return result
    
    def train_intents(self, training_data: List[Dict[str, Any]]):
        """
        Train the intent classifier with labeled data.
        
        Args:
            training_data: List of training examples with intents
        """
        self.intent_classifier.train(training_data)
    
    def add_entity_pattern(self, entity_type: str, pattern: str):
        """
        Add a pattern for entity extraction.
        
        Args:
            entity_type: Type of entity
            pattern: Regex pattern or keyword
        """
        self.entity_extractor.add_pattern(entity_type, pattern)
    
    def clear_context(self, user_id: str):
        """
        Clear conversation context for a user.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.context_manager.clear_context(user_id)
