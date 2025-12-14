"""Web/REST API connector implementation."""
from typing import Dict, Any, Optional
from .base_connector import BaseConnector


class WebConnector(BaseConnector):
    """
    Web connector for REST API integration.
    
    Provides a simple interface for web-based chatbot interactions.
    """
    
    def __init__(self, engine, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the web connector.
        
        Args:
            engine: ChatbotEngine instance
            config: Configuration dictionary
        """
        super().__init__(engine, config)
        self.message_queue = []
    
    def connect(self):
        """Establish connection (always available for web)."""
        self.connected = True
        return True
    
    def disconnect(self):
        """Disconnect (no-op for web)."""
        self.connected = False
    
    def send_message(self, user_id: str, message: str, **kwargs):
        """
        Queue a message for sending.
        
        Args:
            user_id: Unique identifier for the user
            message: Message to send
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with message status
        """
        response = {
            "user_id": user_id,
            "message": message,
            "timestamp": kwargs.get("timestamp"),
        }
        self.message_queue.append(response)
        return response
    
    def receive_message(self) -> Optional[Dict[str, Any]]:
        """
        Receive a message (not applicable for REST API).
        
        Returns:
            None (messages come via handle_request)
        """
        return None
    
    def handle_request(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Handle a web request synchronously.
        
        Args:
            user_id: Unique identifier for the user
            message: User's message
        
        Returns:
            Processing result with response
        """
        result = self.process_incoming_message({
            "user_id": user_id,
            "message": message,
        })
        
        # Generate response message if handler provided one
        if "response" in result:
            response_text = result["response"]
        else:
            response_text = f"Understood: {result.get('intent', 'unknown')}"
        
        return {
            "success": True,
            "response": response_text,
            "intent": result.get("intent"),
            "confidence": result.get("confidence"),
            "entities": result.get("entities", []),
        }
