"""Conversation summarization for memory management"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ConversationSummarizer:
    """Summarizes conversations to reduce memory footprint"""
    
    def __init__(self, threshold: int = 10):
        """Initialize summarizer
        
        Args:
            threshold: Number of messages before summarization
        """
        self.threshold = threshold
        
    def should_summarize(self, message_count: int) -> bool:
        """Check if conversation should be summarized
        
        Args:
            message_count: Number of messages in conversation
            
        Returns:
            True if summarization is needed
        """
        return message_count >= self.threshold
    
    def summarize(self, messages: List[Dict[str, Any]]) -> str:
        """Summarize conversation messages
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Summary text
        """
        if not messages:
            return "No conversation to summarize."
        
        # Extract key information
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        intents = [msg.get("intent") for msg in messages if "intent" in msg]
        
        # Generate simple summary
        summary_parts = [
            f"Conversation with {len(messages)} messages.",
            f"User sent {len(user_messages)} messages.",
        ]
        
        if intents:
            intent_counts = {}
            for intent in intents:
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            most_common = max(intent_counts.items(), key=lambda x: x[1])
            summary_parts.append(f"Main topic: {most_common[0]} ({most_common[1]} times).")
        
        summary = " ".join(summary_parts)
        logger.info(f"Generated conversation summary: {summary}")
        
        return summary
    
    def extract_key_points(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract key points from conversation
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of key points
        """
        key_points = []
        
        # Extract important intents
        important_intents = ["complaint", "request", "question"]
        for msg in messages:
            intent = msg.get("intent")
            if intent in important_intents:
                content = msg.get("content", "")
                if content:
                    key_points.append(f"{intent.capitalize()}: {content[:100]}")
        
        return key_points
    
    def create_compact_history(
        self,
        messages: List[Dict[str, Any]],
        max_messages: int = 5
    ) -> List[Dict[str, Any]]:
        """Create compact version of conversation history
        
        Args:
            messages: Full message list
            max_messages: Maximum messages to keep
            
        Returns:
            Compacted message list with summary
        """
        if len(messages) <= max_messages:
            return messages
        
        # Keep most recent messages
        recent_messages = messages[-max_messages:]
        
        # Summarize older messages
        older_messages = messages[:-max_messages]
        summary = self.summarize(older_messages)
        
        # Create summary message
        summary_msg = {
            "role": "system",
            "content": f"[Summary of earlier conversation: {summary}]",
            "timestamp": older_messages[0].get("timestamp") if older_messages else None
        }
        
        return [summary_msg] + recent_messages


# Global instance
_summarizer = None


def get_summarizer() -> ConversationSummarizer:
    """Get or create the global summarizer instance"""
    global _summarizer
    if _summarizer is None:
        from app.core.config import settings
        _summarizer = ConversationSummarizer(threshold=settings.conversation_summary_threshold)
    return _summarizer
