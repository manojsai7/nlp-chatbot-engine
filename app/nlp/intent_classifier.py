"""Intent classification module using transformer models"""
import logging
from typing import Dict, List, Tuple

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

from app.core.config import settings

logger = logging.getLogger(__name__)


class IntentClassifier:
    """Intent classification using transformer models"""
    
    def __init__(self, model_name: str = None):
        """Initialize the intent classifier
        
        Args:
            model_name: HuggingFace model name or path
        """
        self.model_name = model_name or settings.intent_model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Default intents for demo purposes
        self.intent_labels = [
            "greeting",
            "farewell",
            "question",
            "complaint",
            "request",
            "feedback",
            "help",
            "small_talk",
            "unknown"
        ]
        
        # Initialize model and tokenizer (lazy loading)
        self.tokenizer = None
        self.model = None
        self._is_initialized = False
        
    def initialize(self):
        """Lazy initialization of model"""
        if self._is_initialized:
            return
        
        if not TORCH_AVAILABLE:
            logger.warning("PyTorch/Transformers not available. Using rule-based fallback only.")
            self._is_initialized = False
            return
            
        try:
            logger.info(f"Loading intent classification model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=len(self.intent_labels)
            )
            self.model.to(self.device)
            self.model.eval()
            self._is_initialized = True
            logger.info("Intent classifier initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to load transformer model: {e}. Using rule-based fallback.")
            self._is_initialized = False
    
    def classify(self, text: str) -> Tuple[str, float]:
        """Classify intent of the given text
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        if not self._is_initialized:
            # Use rule-based fallback
            return self._rule_based_classify(text)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=settings.max_sequence_length,
                padding=True
            ).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                confidence, predicted_idx = torch.max(predictions, dim=1)
                
            intent = self.intent_labels[predicted_idx.item()]
            confidence_score = confidence.item()
            
            logger.debug(f"Classified intent: {intent} (confidence: {confidence_score:.3f})")
            return intent, confidence_score
            
        except Exception as e:
            logger.error(f"Error during intent classification: {e}")
            return self._rule_based_classify(text)
    
    def _rule_based_classify(self, text: str) -> Tuple[str, float]:
        """Simple rule-based intent classification fallback
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        text_lower = text.lower().strip()
        
        # Greeting patterns
        if any(word in text_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "greeting", 0.85
        
        # Farewell patterns
        if any(word in text_lower for word in ["bye", "goodbye", "see you", "farewell"]):
            return "farewell", 0.85
        
        # Question patterns
        if text.strip().endswith("?") or any(word in text_lower for word in ["what", "where", "when", "why", "how", "who"]):
            return "question", 0.80
        
        # Help patterns
        if any(word in text_lower for word in ["help", "assist", "support"]):
            return "help", 0.80
        
        # Complaint patterns
        if any(word in text_lower for word in ["complaint", "problem", "issue", "not working", "broken"]):
            return "complaint", 0.75
        
        # Request patterns
        if any(word in text_lower for word in ["please", "can you", "could you", "would you", "i want", "i need"]):
            return "request", 0.75
        
        # Default to unknown
        return "unknown", 0.50
    
    def batch_classify(self, texts: List[str]) -> List[Tuple[str, float]]:
        """Classify multiple texts at once
        
        Args:
            texts: List of input texts
            
        Returns:
            List of (intent_name, confidence_score) tuples
        """
        return [self.classify(text) for text in texts]


# Global instance
_intent_classifier = None


def get_intent_classifier() -> IntentClassifier:
    """Get or create the global intent classifier instance"""
    global _intent_classifier
    if _intent_classifier is None:
        _intent_classifier = IntentClassifier()
        _intent_classifier.initialize()
    return _intent_classifier
