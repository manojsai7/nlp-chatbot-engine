"""Base adapter interface"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAdapter(ABC):
    """Abstract base class for channel adapters"""
    
    @abstractmethod
    async def send_message(self, recipient: str, message: str, **kwargs) -> bool:
        """Send a message through the channel
        
        Args:
            recipient: Recipient identifier
            message: Message text
            **kwargs: Additional channel-specific parameters
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def receive_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming message
        
        Args:
            payload: Raw message payload from the channel
            
        Returns:
            Normalized message dictionary
        """
        pass
    
    def validate_config(self) -> bool:
        """Validate adapter configuration
        
        Returns:
            True if configuration is valid
        """
        return True
