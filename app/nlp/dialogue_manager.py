"""Dialogue management module for conversation flow"""
import logging
from typing import Dict, Any, Optional, List
import random

from app.core.models import Intent, Entity

logger = logging.getLogger(__name__)


class DialogueManager:
    """Manages conversation flow and generates responses"""
    
    def __init__(self):
        """Initialize dialogue manager"""
        self.response_templates = self._load_response_templates()
        
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load response templates for different intents
        
        Returns:
            Dictionary mapping intents to response templates
        """
        return {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to assist you.",
                "Greetings! How may I assist you today?"
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "Bye! Feel free to come back anytime.",
                "See you later! Take care!",
                "Farewell! It was nice talking to you."
            ],
            "question": [
                "That's a great question. Let me help you with that.",
                "I'd be happy to answer that for you.",
                "Let me look into that for you.",
                "I'll do my best to answer your question."
            ],
            "help": [
                "I'm here to help! What do you need assistance with?",
                "Of course! I'd be glad to help you.",
                "I can assist you with that. What specifically do you need help with?",
                "Let me help you with that. What can I do for you?"
            ],
            "complaint": [
                "I'm sorry to hear you're experiencing issues. Let me help resolve this.",
                "I apologize for the inconvenience. I'll do my best to help.",
                "Thank you for bringing this to my attention. Let's work on fixing this.",
                "I understand your concern. Let me assist you with this problem."
            ],
            "request": [
                "I'll be happy to help with your request.",
                "Let me assist you with that.",
                "I can help you with that request.",
                "Sure, I'll help you with that."
            ],
            "feedback": [
                "Thank you for your feedback! We appreciate it.",
                "I appreciate you sharing your thoughts.",
                "Thanks for letting us know. Your feedback is valuable.",
                "Thank you! We value your feedback."
            ],
            "small_talk": [
                "I'm doing well, thank you for asking!",
                "That's interesting! Tell me more.",
                "I appreciate the conversation!",
                "That's nice to hear!"
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase that?",
                "I didn't quite get that. Can you provide more details?",
                "I'm sorry, I'm not sure how to respond to that. Can you clarify?",
                "Could you explain that differently? I want to make sure I understand."
            ]
        }
    
    def generate_response(
        self,
        intent: str,
        confidence: float,
        entities: Optional[List[Entity]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate response based on intent and context
        
        Args:
            intent: Detected intent
            confidence: Confidence score
            entities: Extracted entities
            context: Additional context
            
        Returns:
            Response dictionary with text and metadata
        """
        # Get response template
        templates = self.response_templates.get(intent, self.response_templates["unknown"])
        response_text = random.choice(templates)
        
        # Enhance response with entity information
        if entities and len(entities) > 0:
            entity_info = self._format_entities(entities)
            if entity_info:
                response_text += f" {entity_info}"
        
        # Add suggestions based on intent
        suggestions = self._generate_suggestions(intent)
        
        result = {
            "response": response_text,
            "confidence": confidence,
            "suggestions": suggestions,
            "metadata": {
                "intent": intent,
                "entity_count": len(entities) if entities else 0
            }
        }
        
        logger.debug(f"Generated response for intent '{intent}'")
        return result
    
    def _format_entities(self, entities: List[Entity]) -> str:
        """Format entity information for response
        
        Args:
            entities: List of entities
            
        Returns:
            Formatted string with entity information
        """
        if not entities:
            return ""
        
        # Group entities by type
        entity_groups = {}
        for entity in entities:
            if entity.label not in entity_groups:
                entity_groups[entity.label] = []
            entity_groups[entity.label].append(entity.text)
        
        # Format entity information
        parts = []
        for label, texts in entity_groups.items():
            if len(texts) == 1:
                parts.append(f"I noticed you mentioned {texts[0]} ({label}).")
            else:
                parts.append(f"I noticed you mentioned {', '.join(texts)} ({label}).")
        
        return " ".join(parts) if parts else ""
    
    def _generate_suggestions(self, intent: str) -> List[str]:
        """Generate follow-up suggestions based on intent
        
        Args:
            intent: Current intent
            
        Returns:
            List of suggestion strings
        """
        suggestions_map = {
            "greeting": [
                "I can help you with questions",
                "Tell me what you need",
                "Ask me anything"
            ],
            "question": [
                "Do you need more information?",
                "Would you like to know anything else?",
                "Any other questions?"
            ],
            "help": [
                "What specifically do you need help with?",
                "I can guide you through the process",
                "Let me know if you need clarification"
            ],
            "complaint": [
                "Would you like to speak with a supervisor?",
                "Can I help resolve this issue?",
                "Would you like to provide more details?"
            ]
        }
        
        return suggestions_map.get(intent, [])
    
    def manage_context(
        self,
        current_intent: str,
        conversation_history: List[Dict[str, Any]],
        max_history: int = 5
    ) -> Dict[str, Any]:
        """Manage conversation context
        
        Args:
            current_intent: Current intent
            conversation_history: Previous conversation turns
            max_history: Maximum history to consider
            
        Returns:
            Context dictionary
        """
        recent_history = conversation_history[-max_history:] if conversation_history else []
        
        # Extract patterns from history
        intents_in_history = [turn.get("intent") for turn in recent_history if "intent" in turn]
        
        context = {
            "turn_count": len(conversation_history),
            "recent_intents": intents_in_history,
            "is_follow_up": len(intents_in_history) > 0 and intents_in_history[-1] == current_intent
        }
        
        return context


# Global instance
_dialogue_manager = None


def get_dialogue_manager() -> DialogueManager:
    """Get or create the global dialogue manager instance"""
    global _dialogue_manager
    if _dialogue_manager is None:
        _dialogue_manager = DialogueManager()
    return _dialogue_manager
