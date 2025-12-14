"""Tests for ContextManager."""
import pytest
from nlp_chatbot_engine.memory.context_manager import ContextManager
import time


def test_context_manager_initialization():
    """Test context manager initializes correctly."""
    manager = ContextManager()
    assert manager.contexts is not None
    assert manager.context_timeout is None


def test_get_context_new_user():
    """Test getting context for new user."""
    manager = ContextManager()
    context = manager.get_context("user1")
    
    assert context == {}
    assert "user1" in manager.contexts


def test_update_context():
    """Test updating context."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key": "value"})
    context = manager.get_context("user1")
    
    assert context["key"] == "value"


def test_update_context_merge():
    """Test merging context updates."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key1": "value1"})
    manager.update_context("user1", {"key2": "value2"}, merge=True)
    
    context = manager.get_context("user1")
    assert context["key1"] == "value1"
    assert context["key2"] == "value2"


def test_update_context_replace():
    """Test replacing context."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key1": "value1"})
    manager.update_context("user1", {"key2": "value2"}, merge=False)
    
    context = manager.get_context("user1")
    assert "key1" not in context
    assert context["key2"] == "value2"


def test_set_context_value():
    """Test setting specific context value."""
    manager = ContextManager()
    
    manager.set_context_value("user1", "test_key", "test_value")
    value = manager.get_context_value("user1", "test_key")
    
    assert value == "test_value"


def test_get_context_value_default():
    """Test getting context value with default."""
    manager = ContextManager()
    
    value = manager.get_context_value("user1", "nonexistent", "default")
    assert value == "default"


def test_has_context():
    """Test checking if user has context."""
    manager = ContextManager()
    
    assert not manager.has_context("user1")
    
    manager.update_context("user1", {"key": "value"})
    assert manager.has_context("user1")


def test_clear_context():
    """Test clearing context."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key": "value"})
    assert manager.has_context("user1")
    
    manager.clear_context("user1")
    assert not manager.has_context("user1")


def test_delete_context_key():
    """Test deleting specific context key."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key1": "value1", "key2": "value2"})
    manager.delete_context_key("user1", "key1")
    
    context = manager.get_context("user1")
    assert "key1" not in context
    assert "key2" in context


def test_get_all_users():
    """Test getting all users with context."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key": "value"})
    manager.update_context("user2", {"key": "value"})
    
    users = manager.get_all_users()
    assert "user1" in users
    assert "user2" in users


def test_clear_all_contexts():
    """Test clearing all contexts."""
    manager = ContextManager()
    
    manager.update_context("user1", {"key": "value"})
    manager.update_context("user2", {"key": "value"})
    
    manager.clear_all_contexts()
    
    assert not manager.has_context("user1")
    assert not manager.has_context("user2")
    assert len(manager.get_all_users()) == 0


def test_context_timeout():
    """Test context timeout functionality."""
    manager = ContextManager(context_timeout=1)
    
    manager.update_context("user1", {"key": "value"})
    assert manager.has_context("user1")
    
    # Wait for timeout
    time.sleep(1.5)
    
    # Context should be cleared on next access
    context = manager.get_context("user1")
    assert context == {}
