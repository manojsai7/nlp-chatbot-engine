"""WhatsApp channel adapter using Twilio"""
import logging
from typing import Dict, Any
from app.adapters.base import BaseAdapter
from app.core.config import settings

logger = logging.getLogger(__name__)


class WhatsAppAdapter(BaseAdapter):
    """Adapter for WhatsApp via Twilio"""
    
    def __init__(
        self,
        account_sid: str = None,
        auth_token: str = None,
        whatsapp_number: str = None
    ):
        """Initialize WhatsApp adapter
        
        Args:
            account_sid: Twilio account SID
            auth_token: Twilio auth token
            whatsapp_number: Twilio WhatsApp number
        """
        self.account_sid = account_sid or settings.twilio_account_sid
        self.auth_token = auth_token or settings.twilio_auth_token
        self.whatsapp_number = whatsapp_number or settings.twilio_whatsapp_number
        self.channel_name = "whatsapp"
        self.client = None
        self._is_initialized = False
        
    def initialize(self):
        """Initialize Twilio client"""
        if self._is_initialized or not self.account_sid:
            return
            
        try:
            from twilio.rest import Client
            logger.info("Initializing Twilio client for WhatsApp")
            self.client = Client(self.account_sid, self.auth_token)
            self._is_initialized = True
            logger.info("WhatsApp adapter initialized successfully")
        except ImportError:
            logger.error("twilio not installed. Install with: pip install twilio")
        except Exception as e:
            logger.error(f"Error initializing Twilio client: {e}")
    
    async def send_message(self, recipient: str, message: str, **kwargs) -> bool:
        """Send message via WhatsApp
        
        Args:
            recipient: Recipient phone number (format: whatsapp:+1234567890)
            message: Message text
            **kwargs: Additional Twilio parameters
            
        Returns:
            True if successful
        """
        if not self._is_initialized:
            self.initialize()
        
        if not self._is_initialized:
            logger.warning("WhatsApp adapter not initialized")
            return False
        
        try:
            # Ensure recipient has whatsapp: prefix
            if not recipient.startswith("whatsapp:"):
                recipient = f"whatsapp:{recipient}"
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=recipient,
                **kwargs
            )
            
            logger.debug(f"Sent WhatsApp message to {recipient}: {message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    async def receive_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming WhatsApp message
        
        Args:
            payload: Twilio webhook payload
            
        Returns:
            Normalized message
        """
        # Extract phone number without whatsapp: prefix
        from_number = payload.get("From", "").replace("whatsapp:", "")
        
        return {
            "text": payload.get("Body", ""),
            "user_id": from_number,
            "session_id": from_number,  # Use phone number as session
            "channel": self.channel_name,
            "metadata": {
                "message_sid": payload.get("MessageSid"),
                "account_sid": payload.get("AccountSid"),
                "from": payload.get("From"),
                "to": payload.get("To"),
                "media_count": payload.get("NumMedia", 0)
            }
        }
    
    def validate_config(self) -> bool:
        """Validate WhatsApp configuration"""
        return bool(
            self.account_sid and
            self.auth_token and
            self.whatsapp_number
        )


# Global instance
_whatsapp_adapter = None


def get_whatsapp_adapter() -> WhatsAppAdapter:
    """Get or create the global WhatsApp adapter instance"""
    global _whatsapp_adapter
    if _whatsapp_adapter is None:
        _whatsapp_adapter = WhatsAppAdapter()
        _whatsapp_adapter.initialize()
    return _whatsapp_adapter
