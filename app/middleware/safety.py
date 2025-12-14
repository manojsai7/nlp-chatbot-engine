"""Safety filter middleware for content moderation"""
import logging
import re
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SafetyFilter:
    """Content safety and moderation filter"""
    
    def __init__(self):
        """Initialize safety filter"""
        self.blocked_patterns = self._load_blocked_patterns()
        self.toxic_keywords = self._load_toxic_keywords()
        
    def _load_blocked_patterns(self) -> List[re.Pattern]:
        """Load blocked regex patterns
        
        Returns:
            List of compiled regex patterns
        """
        # In production, load from configuration or database
        patterns = [
            r'\b(?:spam|scam)\b',
            r'\b(?:credit\s*card\s*number)\b',
            r'\b(?:ssn|social\s*security)\b',
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def _load_toxic_keywords(self) -> List[str]:
        """Load toxic keywords list
        
        Returns:
            List of toxic keywords
        """
        # In production, load from comprehensive list
        return [
            "abuse",
            "threat",
            "violence",
            "hate"
        ]
    
    def is_safe(self, text: str) -> bool:
        """Check if text is safe
        
        Args:
            text: Input text to check
            
        Returns:
            True if safe, False if unsafe
        """
        # Check blocked patterns
        for pattern in self.blocked_patterns:
            if pattern.search(text):
                logger.warning(f"Blocked pattern detected in text")
                return False
        
        # Check toxic keywords (simple check)
        text_lower = text.lower()
        for keyword in self.toxic_keywords:
            if keyword in text_lower:
                logger.warning(f"Toxic keyword detected: {keyword}")
                return False
        
        return True
    
    def filter_content(self, text: str) -> Dict[str, any]:
        """Filter and analyze content
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with safety analysis
        """
        is_safe = self.is_safe(text)
        
        result = {
            "is_safe": is_safe,
            "original_text": text,
            "filtered_text": text if is_safe else "[Content filtered]",
            "flags": []
        }
        
        # Check for PII
        if self._contains_pii(text):
            result["flags"].append("possible_pii")
        
        # Check for sensitive information
        if self._contains_sensitive_info(text):
            result["flags"].append("sensitive_info")
        
        return result
    
    def _contains_pii(self, text: str) -> bool:
        """Check for personally identifiable information
        
        Args:
            text: Input text
            
        Returns:
            True if PII detected
        """
        # Simple email detection
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, text):
            return True
        
        # Simple phone number detection
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, text):
            return True
        
        return False
    
    def _contains_sensitive_info(self, text: str) -> bool:
        """Check for sensitive information
        
        Args:
            text: Input text
            
        Returns:
            True if sensitive info detected
        """
        sensitive_keywords = [
            "password",
            "credit card",
            "bank account",
            "pin code"
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in sensitive_keywords)


# Global instance
_safety_filter = None


def get_safety_filter() -> SafetyFilter:
    """Get or create the global safety filter instance"""
    global _safety_filter
    if _safety_filter is None:
        _safety_filter = SafetyFilter()
    return _safety_filter
