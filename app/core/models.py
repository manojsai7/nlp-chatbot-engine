"""Pydantic models for API requests and responses"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    """Message model"""
    text: str
    user_id: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class Intent(BaseModel):
    """Intent classification result"""
    name: str
    confidence: float
    entities: Optional[List[Dict[str, Any]]] = None


class Entity(BaseModel):
    """Named entity"""
    text: str
    label: str
    start: int
    end: int
    confidence: Optional[float] = None


class ChatRequest(BaseModel):
    """Chat request payload"""
    message: str
    user_id: str
    session_id: Optional[str] = None
    channel: str = "web"
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response payload"""
    response: str
    intent: Optional[Intent] = None
    entities: Optional[List[Entity]] = None
    session_id: str
    confidence: float
    suggestions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ConversationHistory(BaseModel):
    """Conversation history"""
    session_id: str
    user_id: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
