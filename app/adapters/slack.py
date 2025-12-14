"""Slack channel adapter"""
import logging
from typing import Dict, Any, Optional
from app.adapters.base import BaseAdapter
from app.core.config import settings

logger = logging.getLogger(__name__)


class SlackAdapter(BaseAdapter):
    """Adapter for Slack messaging platform"""
    
    def __init__(self, bot_token: str = None, signing_secret: str = None):
        """Initialize Slack adapter
        
        Args:
            bot_token: Slack bot token
            signing_secret: Slack signing secret
        """
        self.bot_token = bot_token or settings.slack_bot_token
        self.signing_secret = signing_secret or settings.slack_signing_secret
        self.channel_name = "slack"
        self.client = None
        self._is_initialized = False
        
    def initialize(self):
        """Initialize Slack client"""
        if self._is_initialized or not self.bot_token:
            return
            
        try:
            from slack_sdk import WebClient
            logger.info("Initializing Slack client")
            self.client = WebClient(token=self.bot_token)
            self._is_initialized = True
            logger.info("Slack adapter initialized successfully")
        except ImportError:
            logger.error("slack-sdk not installed. Install with: pip install slack-sdk")
        except Exception as e:
            logger.error(f"Error initializing Slack client: {e}")
    
    async def send_message(self, recipient: str, message: str, **kwargs) -> bool:
        """Send message to Slack
        
        Args:
            recipient: Slack channel ID
            message: Message text
            **kwargs: Additional Slack parameters
            
        Returns:
            True if successful
        """
        if not self._is_initialized:
            self.initialize()
        
        if not self._is_initialized:
            logger.warning("Slack adapter not initialized")
            return False
        
        try:
            response = self.client.chat_postMessage(
                channel=recipient,
                text=message,
                **kwargs
            )
            logger.debug(f"Sent message to Slack channel {recipient}")
            return response["ok"]
        except Exception as e:
            logger.error(f"Error sending Slack message: {e}")
            return False
    
    async def receive_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming Slack message
        
        Args:
            payload: Slack event payload
            
        Returns:
            Normalized message
        """
        event = payload.get("event", {})
        
        return {
            "text": event.get("text", ""),
            "user_id": event.get("user", ""),
            "session_id": event.get("channel", ""),
            "channel": self.channel_name,
            "metadata": {
                "channel_id": event.get("channel"),
                "timestamp": event.get("ts"),
                "thread_ts": event.get("thread_ts")
            }
        }
    
    def validate_config(self) -> bool:
        """Validate Slack configuration"""
        return bool(self.bot_token and self.signing_secret)


# Global instance
_slack_adapter = None


def get_slack_adapter() -> SlackAdapter:
    """Get or create the global Slack adapter instance"""
    global _slack_adapter
    if _slack_adapter is None:
        _slack_adapter = SlackAdapter()
        _slack_adapter.initialize()
    return _slack_adapter
