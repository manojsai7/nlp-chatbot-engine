"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_chat_endpoint():
    """Test main chat endpoint"""
    payload = {
        "message": "Hello there!",
        "user_id": "test_user",
        "channel": "web"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "response" in data
    assert "intent" in data
    assert "session_id" in data
    assert data["intent"]["name"] == "greeting"


def test_chat_with_session():
    """Test chat with existing session"""
    payload = {
        "message": "Hi!",
        "user_id": "test_user",
        "session_id": "test_session_123",
        "channel": "web"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["session_id"] == "test_session_123"


def test_get_conversation():
    """Test getting conversation history"""
    # First, send a message
    payload = {
        "message": "Hello",
        "user_id": "test_user",
        "session_id": "history_test",
        "channel": "web"
    }
    client.post("/api/v1/chat", json=payload)
    
    # Get conversation history
    response = client.get("/api/v1/conversation/history_test")
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert "messages" in data


def test_clear_conversation():
    """Test clearing conversation history"""
    response = client.delete("/api/v1/conversation/test_session")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data


def test_evaluate_endpoint():
    """Test evaluation endpoint"""
    response = client.get("/api/v1/evaluate")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "results" in data
    assert data["status"] == "completed"
