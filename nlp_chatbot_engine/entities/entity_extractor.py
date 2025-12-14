"""Entity extraction implementation."""
from typing import Dict, List, Optional, Any
import re
from datetime import datetime


class EntityExtractor:
    """
    Entity extraction system for identifying structured information in text.
    
    Supports pattern-based extraction for common entity types.
    """
    
    def __init__(self):
        """Initialize the entity extractor with common patterns."""
        self.patterns = {}
        self.extractors = {}
        
        # Register default extractors
        self._register_default_extractors()
    
    def _register_default_extractors(self):
        """Register common entity extraction patterns."""
        # Email pattern
        self.add_pattern(
            "email",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        
        # Phone pattern (simple)
        self.add_pattern(
            "phone",
            r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        )
        
        # URL pattern
        self.add_pattern(
            "url",
            r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)"
        )
        
        # Number pattern
        self.add_pattern(
            "number",
            r"\b\d+(?:\.\d+)?\b"
        )
        
        # Date pattern (simple formats)
        self.add_pattern(
            "date",
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
        )
    
    def add_pattern(self, entity_type: str, pattern: str):
        """
        Add a regex pattern for entity extraction.
        
        Args:
            entity_type: Type of entity to extract
            pattern: Regex pattern string
        """
        if entity_type not in self.patterns:
            self.patterns[entity_type] = []
        
        self.patterns[entity_type].append(re.compile(pattern, re.IGNORECASE))
    
    def add_custom_extractor(self, entity_type: str, extractor_func: callable):
        """
        Add a custom extraction function.
        
        Args:
            entity_type: Type of entity to extract
            extractor_func: Function that takes text and returns list of entities
        """
        self.extractors[entity_type] = extractor_func
    
    def extract(
        self,
        text: str,
        intent: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract entities from text.
        
        Args:
            text: Input text to extract entities from
            intent: Optional intent context for guided extraction
        
        Returns:
            List of extracted entities with type, value, and position
        """
        entities = []
        
        # Pattern-based extraction
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    entities.append({
                        "type": entity_type,
                        "value": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                    })
        
        # Custom extractors
        for entity_type, extractor in self.extractors.items():
            custom_entities = extractor(text)
            for entity in custom_entities:
                if isinstance(entity, dict):
                    entity["type"] = entity_type
                    entities.append(entity)
                else:
                    entities.append({
                        "type": entity_type,
                        "value": entity,
                    })
        
        # Sort by position if available
        entities.sort(key=lambda x: x.get("start", 0))
        
        return entities
    
    def extract_by_type(
        self,
        text: str,
        entity_type: str
    ) -> List[str]:
        """
        Extract entities of a specific type.
        
        Args:
            text: Input text
            entity_type: Type of entity to extract
        
        Returns:
            List of entity values
        """
        all_entities = self.extract(text)
        return [
            entity["value"]
            for entity in all_entities
            if entity["type"] == entity_type
        ]
    
    def has_entity_type(self, text: str, entity_type: str) -> bool:
        """
        Check if text contains a specific entity type.
        
        Args:
            text: Input text
            entity_type: Type of entity to check for
        
        Returns:
            True if entity type is found
        """
        return len(self.extract_by_type(text, entity_type)) > 0
