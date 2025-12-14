"""Context and conversation memory management."""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class ContextManager:
    """
    Manages conversation context and memory for users.
    
    Stores and retrieves context information across conversations,
    with support for session management and context expiration.
    """
    
    def __init__(self, context_timeout: Optional[int] = None):
        """
        Initialize the context manager.
        
        Args:
            context_timeout: Timeout in seconds for context expiration (None = no expiration)
        """
        self.contexts = defaultdict(dict)
        self.timestamps = {}
        self.context_timeout = context_timeout
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get the conversation context for a user.
        
        Args:
            user_id: Unique identifier for the user
        
        Returns:
            Dictionary containing user context
        """
        # Check for context expiration
        if self.context_timeout and user_id in self.timestamps:
            last_access = self.timestamps[user_id]
            if datetime.now() - last_access > timedelta(seconds=self.context_timeout):
                self.clear_context(user_id)
        
        # Update timestamp
        self.timestamps[user_id] = datetime.now()
        
        return dict(self.contexts[user_id])
    
    def update_context(
        self,
        user_id: str,
        updates: Dict[str, Any],
        merge: bool = True
    ):
        """
        Update the conversation context for a user.
        
        Args:
            user_id: Unique identifier for the user
            updates: Dictionary of context updates
            merge: If True, merge with existing context; if False, replace
        """
        if merge:
            self.contexts[user_id].update(updates)
        else:
            self.contexts[user_id] = dict(updates)
        
        self.timestamps[user_id] = datetime.now()
    
    def set_context_value(self, user_id: str, key: str, value: Any):
        """
        Set a specific context value.
        
        Args:
            user_id: Unique identifier for the user
            key: Context key
            value: Value to store
        """
        self.contexts[user_id][key] = value
        self.timestamps[user_id] = datetime.now()
    
    def get_context_value(
        self,
        user_id: str,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get a specific context value.
        
        Args:
            user_id: Unique identifier for the user
            key: Context key
            default: Default value if key not found
        
        Returns:
            Context value or default
        """
        return self.contexts[user_id].get(key, default)
    
    def has_context(self, user_id: str) -> bool:
        """
        Check if a user has active context.
        
        Args:
            user_id: Unique identifier for the user
        
        Returns:
            True if user has context
        """
        return user_id in self.contexts and bool(self.contexts[user_id])
    
    def clear_context(self, user_id: str):
        """
        Clear all context for a user.
        
        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.contexts:
            self.contexts[user_id].clear()
        if user_id in self.timestamps:
            del self.timestamps[user_id]
    
    def delete_context_key(self, user_id: str, key: str):
        """
        Delete a specific context key.
        
        Args:
            user_id: Unique identifier for the user
            key: Context key to delete
        """
        if user_id in self.contexts and key in self.contexts[user_id]:
            del self.contexts[user_id][key]
    
    def get_all_users(self) -> list:
        """
        Get list of all users with active context.
        
        Returns:
            List of user IDs
        """
        return list(self.contexts.keys())
    
    def clear_all_contexts(self):
        """Clear all contexts for all users."""
        self.contexts.clear()
        self.timestamps.clear()
