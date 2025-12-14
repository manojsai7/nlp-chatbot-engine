"""Long-term memory management using database"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()


class ConversationRecord(Base):
    """Database model for conversation records"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), index=True)
    user_id = Column(String(255), index=True)
    message = Column(Text)
    intent = Column(String(100))
    confidence = Column(Float)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class LongTermMemory:
    """Long-term memory storage using SQL database"""
    
    def __init__(self, database_url: str = None):
        """Initialize long-term memory
        
        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url or settings.database_url
        self.engine = None
        self.SessionLocal = None
        self._is_initialized = False
        
    def initialize(self):
        """Initialize database connection and tables"""
        if self._is_initialized:
            return
            
        try:
            logger.info(f"Initializing database: {self.database_url}")
            self.engine = create_engine(self.database_url)
            Base.metadata.create_all(bind=self.engine)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self._is_initialized = True
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            self._is_initialized = False
    
    def store_conversation(
        self,
        session_id: str,
        user_id: str,
        message: str,
        intent: str,
        confidence: float,
        response: str
    ):
        """Store conversation in long-term memory
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            message: User message
            intent: Detected intent
            confidence: Intent confidence
            response: Bot response
        """
        if not self._is_initialized:
            self.initialize()
        
        if not self._is_initialized:
            logger.warning("Database not initialized, skipping storage")
            return
        
        try:
            db = self.SessionLocal()
            record = ConversationRecord(
                session_id=session_id,
                user_id=user_id,
                message=message,
                intent=intent,
                confidence=confidence,
                response=response
            )
            db.add(record)
            db.commit()
            db.close()
            
            logger.debug(f"Stored conversation record for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
    
    def get_user_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve user's conversation history
        
        Args:
            user_id: User identifier
            limit: Maximum number of records
            
        Returns:
            List of conversation records
        """
        if not self._is_initialized:
            return []
        
        try:
            db = self.SessionLocal()
            records = db.query(ConversationRecord)\
                .filter(ConversationRecord.user_id == user_id)\
                .order_by(ConversationRecord.timestamp.desc())\
                .limit(limit)\
                .all()
            
            result = []
            for record in records:
                result.append({
                    "session_id": record.session_id,
                    "message": record.message,
                    "intent": record.intent,
                    "confidence": record.confidence,
                    "response": record.response,
                    "timestamp": record.timestamp.isoformat()
                })
            
            db.close()
            logger.debug(f"Retrieved {len(result)} records for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error retrieving user history: {e}")
            return []
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieve session conversation history
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of conversation records
        """
        if not self._is_initialized:
            return []
        
        try:
            db = self.SessionLocal()
            records = db.query(ConversationRecord)\
                .filter(ConversationRecord.session_id == session_id)\
                .order_by(ConversationRecord.timestamp.asc())\
                .all()
            
            result = []
            for record in records:
                result.append({
                    "message": record.message,
                    "intent": record.intent,
                    "confidence": record.confidence,
                    "response": record.response,
                    "timestamp": record.timestamp.isoformat()
                })
            
            db.close()
            logger.debug(f"Retrieved {len(result)} records for session {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error retrieving session history: {e}")
            return []


# Global instance
_long_term_memory = None


def get_long_term_memory() -> LongTermMemory:
    """Get or create the global long-term memory instance"""
    global _long_term_memory
    if _long_term_memory is None:
        _long_term_memory = LongTermMemory()
        if settings.long_term_memory_enabled:
            _long_term_memory.initialize()
    return _long_term_memory
