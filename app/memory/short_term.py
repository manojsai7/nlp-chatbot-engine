"""Short-term memory management using Redis"""
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ShortTermMemory:
    """Short-term conversation memory using Redis"""
    
    def __init__(self, redis_client=None, ttl: int = 3600):
        """Initialize short-term memory
        
        Args:
            redis_client: Redis client instance
            ttl: Time to live in seconds
        """
        self.redis_client = redis_client
        self.ttl = ttl
        self._is_initialized = False
        
    def initialize(self):
        """Initialize Redis connection"""
        if self._is_initialized:
            return
            
        if self.redis_client is None:
            try:
                import redis
                from app.core.config import settings
                
                logger.info(f"Connecting to Redis at {settings.redis_host}:{settings.redis_port}")
                self.redis_client = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    db=settings.redis_db,
                    password=settings.redis_password,
                    decode_responses=True
                )
                self.redis_client.ping()
                self._is_initialized = True
                logger.info("Redis connection established")
            except Exception as e:
                logger.warning(f"Redis not available: {e}. Using in-memory fallback.")
                self._is_initialized = False
    
    def store_message(self, session_id: str, user_id: str, message: str, role: str = "user"):
        """Store a message in short-term memory
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            message: Message text
            role: Message role (user or assistant)
        """
        try:
            if not self._is_initialized:
                self.initialize()
            
            if not self._is_initialized:
                # Fallback: just log
                logger.debug(f"Would store message for session {session_id}")
                return
            
            key = f"session:{session_id}:messages"
            message_data = {
                "role": role,
                "content": message,
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id
            }
            
            # Add to list
            self.redis_client.rpush(key, json.dumps(message_data))
            self.redis_client.expire(key, self.ttl)
            
            logger.debug(f"Stored message for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error storing message: {e}")
    
    def get_conversation(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve conversation history
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of messages
        """
        try:
            if not self._is_initialized:
                return []
            
            key = f"session:{session_id}:messages"
            messages_raw = self.redis_client.lrange(key, -limit, -1)
            
            messages = []
            for msg_str in messages_raw:
                try:
                    messages.append(json.loads(msg_str))
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse message: {msg_str}")
            
            logger.debug(f"Retrieved {len(messages)} messages for session {session_id}")
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving conversation: {e}")
            return []
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history
        
        Args:
            session_id: Session identifier
        """
        try:
            if not self._is_initialized:
                return
            
            key = f"session:{session_id}:messages"
            self.redis_client.delete(key)
            logger.info(f"Cleared conversation for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get session metadata
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session information
        """
        try:
            if not self._is_initialized:
                return {}
            
            key = f"session:{session_id}:messages"
            message_count = self.redis_client.llen(key)
            ttl = self.redis_client.ttl(key)
            
            return {
                "session_id": session_id,
                "message_count": message_count,
                "ttl": ttl
            }
            
        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return {}


# Global instance
_short_term_memory = None


def get_short_term_memory() -> ShortTermMemory:
    """Get or create the global short-term memory instance"""
    global _short_term_memory
    if _short_term_memory is None:
        from app.core.config import settings
        _short_term_memory = ShortTermMemory(ttl=settings.short_term_memory_ttl)
        _short_term_memory.initialize()
    return _short_term_memory
