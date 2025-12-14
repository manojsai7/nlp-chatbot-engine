"""Intent classification implementation."""
from typing import Dict, Any, List, Optional
import re
from collections import defaultdict


class IntentClassifier:
    """
    Intent classification system for identifying user intentions.
    
    Supports both keyword-based and ML-based classification.
    """
    
    def __init__(self):
        """Initialize the intent classifier."""
        self.intents = {}
        self.keywords = defaultdict(list)
        self.patterns = defaultdict(list)
        self.trained = False
        self.default_intent = "unknown"
    
    def add_intent(
        self,
        intent: str,
        keywords: Optional[List[str]] = None,
        patterns: Optional[List[str]] = None
    ):
        """
        Add an intent with associated keywords and patterns.
        
        Args:
            intent: Intent name
            keywords: List of keywords associated with the intent
            patterns: List of regex patterns for matching
        """
        self.intents[intent] = {
            "keywords": keywords or [],
            "patterns": patterns or [],
        }
        
        if keywords:
            self.keywords[intent].extend(keywords)
        
        if patterns:
            for pattern in patterns:
                self.patterns[intent].append(re.compile(pattern, re.IGNORECASE))
    
    def train(self, training_data: List[Dict[str, Any]]):
        """
        Train the classifier with labeled data.
        
        Args:
            training_data: List of dicts with 'text' and 'intent' keys
        """
        # Simple keyword extraction from training data
        for example in training_data:
            text = example.get("text", "")
            intent = example.get("intent")
            
            if intent:
                # Extract significant words (simple approach)
                words = text.lower().split()
                # Filter out common words
                significant_words = [
                    w for w in words
                    if len(w) > 3 and w not in ["this", "that", "with", "from", "have"]
                ]
                
                if intent not in self.intents:
                    self.intents[intent] = {"keywords": [], "patterns": []}
                
                for word in significant_words:
                    if word not in self.keywords[intent]:
                        self.keywords[intent].append(word)
        
        self.trained = True
    
    def classify(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Classify the intent of a text message.
        
        Args:
            text: Input text to classify
            context: Conversation context
        
        Returns:
            Dictionary with 'intent' and 'confidence' keys
        """
        text_lower = text.lower()
        scores = defaultdict(float)
        
        # Pattern matching (highest priority)
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    scores[intent] += 2.0
        
        # Keyword matching
        words = set(text_lower.split())
        for intent, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    scores[intent] += 1.0
        
        # Context-based boosting
        if context and "last_intent" in context:
            last_intent = context["last_intent"]
            if last_intent in scores:
                scores[last_intent] += 0.3
        
        # Determine best intent
        if scores:
            best_intent = max(scores.items(), key=lambda x: x[1])
            # Normalize confidence to 0-1 range
            confidence = min(best_intent[1] / 3.0, 1.0)
            
            return {
                "intent": best_intent[0],
                "confidence": confidence,
            }
        
        return {
            "intent": self.default_intent,
            "confidence": 0.0,
        }
    
    def get_intents(self) -> List[str]:
        """
        Get list of all registered intents.
        
        Returns:
            List of intent names
        """
        return list(self.intents.keys())
