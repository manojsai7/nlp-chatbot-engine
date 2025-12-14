# Configuration settings for the NLP Chatbot Engine
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # App settings
    app_name: str = "NLP Chatbot Engine"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API settings
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: str = "*"  # Comma-separated list of allowed origins
    
    # NLP settings
    intent_model: str = "distilbert-base-uncased"
    entity_model: str = "en_core_web_sm"
    max_sequence_length: int = 512
    
    # Vector DB settings
    vector_db_type: str = "faiss"  # faiss, chroma, or pgvector
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_dimension: int = 384
    
    # Memory settings
    short_term_memory_ttl: int = 3600  # 1 hour in seconds
    long_term_memory_enabled: bool = True
    conversation_summary_threshold: int = 10  # messages
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Database settings
    database_url: str = "sqlite:///./chatbot.db"
    
    # Security
    safety_filter_enabled: bool = True
    secret_key: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate a secure secret key if not provided
        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe(32)
    
    # Slack adapter
    slack_bot_token: Optional[str] = None
    slack_signing_secret: Optional[str] = None
    
    # Teams adapter
    teams_app_id: Optional[str] = None
    teams_app_password: Optional[str] = None
    
    # WhatsApp adapter (Twilio)
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_number: Optional[str] = None
    
    @property
    def cors_origins_list(self) -> list:
        """Parse CORS origins into a list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
