"""Entity extraction module using spaCy"""
import spacy
from typing import List, Dict, Any
import logging

from app.core.config import settings
from app.core.models import Entity

logger = logging.getLogger(__name__)


class EntityExtractor:
    """Named Entity Recognition using spaCy"""
    
    def __init__(self, model_name: str = None):
        """Initialize the entity extractor
        
        Args:
            model_name: spaCy model name
        """
        self.model_name = model_name or settings.entity_model
        self.nlp = None
        self._is_initialized = False
        
    def initialize(self):
        """Lazy initialization of spaCy model"""
        if self._is_initialized:
            return
            
        try:
            logger.info(f"Loading spaCy model: {self.model_name}")
            self.nlp = spacy.load(self.model_name)
            self._is_initialized = True
            logger.info("Entity extractor initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to load spaCy model: {e}. Using fallback.")
            self._is_initialized = False
    
    def extract(self, text: str) -> List[Entity]:
        """Extract named entities from text
        
        Args:
            text: Input text
            
        Returns:
            List of Entity objects
        """
        if not self._is_initialized:
            return self._rule_based_extract(text)
        
        try:
            doc = self.nlp(text)
            entities = []
            
            for ent in doc.ents:
                entity = Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=None  # spaCy doesn't provide confidence by default
                )
                entities.append(entity)
            
            logger.debug(f"Extracted {len(entities)} entities from text")
            return entities
            
        except Exception as e:
            logger.error(f"Error during entity extraction: {e}")
            return []
    
    def _rule_based_extract(self, text: str) -> List[Entity]:
        """Simple rule-based entity extraction fallback
        
        Args:
            text: Input text
            
        Returns:
            List of Entity objects
        """
        # This is a placeholder for a simple rule-based extractor
        # In production, you would use regex patterns for common entities
        entities = []
        
        # Example: Extract email addresses
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entity = Entity(
                text=match.group(),
                label="EMAIL",
                start=match.start(),
                end=match.end(),
                confidence=0.9
            )
            entities.append(entity)
        
        # Example: Extract phone numbers (simple pattern)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        for match in re.finditer(phone_pattern, text):
            entity = Entity(
                text=match.group(),
                label="PHONE",
                start=match.start(),
                end=match.end(),
                confidence=0.85
            )
            entities.append(entity)
        
        return entities
    
    def extract_with_context(self, text: str) -> Dict[str, Any]:
        """Extract entities with additional context
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with entities and additional context
        """
        entities = self.extract(text)
        
        result = {
            "entities": [entity.model_dump() for entity in entities],
            "entity_count": len(entities),
            "entity_types": list(set(e.label for e in entities))
        }
        
        return result


# Global instance
_entity_extractor = None


def get_entity_extractor() -> EntityExtractor:
    """Get or create the global entity extractor instance"""
    global _entity_extractor
    if _entity_extractor is None:
        _entity_extractor = EntityExtractor()
        _entity_extractor.initialize()
    return _entity_extractor
