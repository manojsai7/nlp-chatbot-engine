"""Web channel adapter"""
import logging
from typing import Dict, Any
from app.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)


class WebAdapter(BaseAdapter):
    """Adapter for web-based chat interface"""
    
    def __init__(self):
        """Initialize web adapter"""
        self.channel_name = "web"
        
    async def send_message(self, recipient: str, message: str, **kwargs) -> bool:
        """Send message to web client
        
        Args:
            recipient: Session or user ID
            message: Message text
            **kwargs: Additional parameters
            
        Returns:
            True if successful
        """
        # In a real implementation, this would push to websocket or SSE
        logger.debug(f"Web adapter sending message to {recipient}")
        return True
    
    async def receive_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming web message
        
        Args:
            payload: Message payload
            
        Returns:
            Normalized message
        """
        return {
            "text": payload.get("message", ""),
            "user_id": payload.get("user_id", ""),
            "session_id": payload.get("session_id", ""),
            "channel": self.channel_name,
            "metadata": payload.get("metadata", {})
        }
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        return True


# Global instance
_web_adapter = None


def get_web_adapter() -> WebAdapter:
    """Get or create the global web adapter instance"""
    global _web_adapter
    if _web_adapter is None:
        _web_adapter = WebAdapter()
    return _web_adapter
