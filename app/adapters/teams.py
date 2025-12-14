"""Microsoft Teams channel adapter"""
import logging
from typing import Dict, Any
from app.adapters.base import BaseAdapter
from app.core.config import settings

logger = logging.getLogger(__name__)


class TeamsAdapter(BaseAdapter):
    """Adapter for Microsoft Teams"""
    
    def __init__(self, app_id: str = None, app_password: str = None):
        """Initialize Teams adapter
        
        Args:
            app_id: Teams app ID
            app_password: Teams app password
        """
        self.app_id = app_id or settings.teams_app_id
        self.app_password = app_password or settings.teams_app_password
        self.channel_name = "teams"
        self._is_initialized = False
        
    def initialize(self):
        """Initialize Teams client"""
        if self._is_initialized or not self.app_id:
            return
            
        try:
            # Teams Bot Framework would be initialized here
            logger.info("Initializing Teams adapter")
            self._is_initialized = True
            logger.info("Teams adapter initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Teams adapter: {e}")
    
    async def send_message(self, recipient: str, message: str, **kwargs) -> bool:
        """Send message to Teams
        
        Args:
            recipient: Teams conversation ID
            message: Message text
            **kwargs: Additional Teams parameters
            
        Returns:
            True if successful
        """
        if not self._is_initialized:
            self.initialize()
        
        if not self._is_initialized:
            logger.warning("Teams adapter not initialized")
            return False
        
        try:
            # Use pymsteams for webhooks or Bot Framework for full bot
            import pymsteams
            
            # This is a simplified example using webhooks
            webhook_url = kwargs.get("webhook_url")
            if webhook_url:
                teams_message = pymsteams.connectorcard(webhook_url)
                teams_message.text(message)
                teams_message.send()
                logger.debug(f"Sent message to Teams")
                return True
            
            logger.warning("No webhook URL provided for Teams message")
            return False
            
        except Exception as e:
            logger.error(f"Error sending Teams message: {e}")
            return False
    
    async def receive_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming Teams message
        
        Args:
            payload: Teams activity payload
            
        Returns:
            Normalized message
        """
        return {
            "text": payload.get("text", ""),
            "user_id": payload.get("from", {}).get("id", ""),
            "session_id": payload.get("conversation", {}).get("id", ""),
            "channel": self.channel_name,
            "metadata": {
                "conversation_id": payload.get("conversation", {}).get("id"),
                "activity_id": payload.get("id"),
                "service_url": payload.get("serviceUrl")
            }
        }
    
    def validate_config(self) -> bool:
        """Validate Teams configuration"""
        return bool(self.app_id and self.app_password)


# Global instance
_teams_adapter = None


def get_teams_adapter() -> TeamsAdapter:
    """Get or create the global Teams adapter instance"""
    global _teams_adapter
    if _teams_adapter is None:
        _teams_adapter = TeamsAdapter()
        _teams_adapter.initialize()
    return _teams_adapter
