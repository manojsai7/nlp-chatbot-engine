"""Base connector interface for multi-channel support."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseConnector(ABC):
    """
    Abstract base class for channel connectors.
    
    All channel-specific connectors should inherit from this class
    and implement the required methods.
    """
    
    def __init__(self, engine, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the connector.
        
        Args:
            engine: ChatbotEngine instance
            config: Connector-specific configuration
        """
        self.engine = engine
        self.config = config or {}
        self.connected = False
    
    @abstractmethod
    def connect(self):
        """
        Establish connection to the channel.
        
        Should set self.connected = True upon successful connection.
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the channel.
        
        Should set self.connected = False upon successful disconnection.
        """
        pass
    
    @abstractmethod
    def send_message(self, user_id: str, message: str, **kwargs):
        """
        Send a message to a user through the channel.
        
        Args:
            user_id: Unique identifier for the user
            message: Message to send
            **kwargs: Additional channel-specific parameters
        """
        pass
    
    @abstractmethod
    def receive_message(self) -> Optional[Dict[str, Any]]:
        """
        Receive a message from the channel.
        
        Returns:
            Dictionary containing message data or None
        """
        pass
    
    def process_incoming_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message through the engine.
        
        Args:
            message_data: Raw message data from the channel
        
        Returns:
            Processing result from the engine
        """
        user_id = message_data.get("user_id")
        message = message_data.get("message")
        
        if not user_id or not message:
            return {"error": "Missing user_id or message"}
        
        # Process through engine
        result = self.engine.process_message(
            message=message,
            user_id=user_id,
            metadata=message_data.get("metadata")
        )
        
        return result
    
    def is_connected(self) -> bool:
        """
        Check if connector is connected.
        
        Returns:
            True if connected
        """
        return self.connected
