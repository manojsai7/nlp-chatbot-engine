"""Embedding generation for RAG"""
import logging
from typing import List
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class Embedder:
    """Generates embeddings for text using sentence transformers"""
    
    def __init__(self, model_name: str = None):
        """Initialize embedder
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name or settings.embedding_model
        self.model = None
        self._is_initialized = False
        
    def initialize(self):
        """Lazy initialization of embedding model"""
        if self._is_initialized:
            return
            
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self._is_initialized = True
            logger.info("Embedding model initialized successfully")
        except ImportError:
            logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
            raise
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector as list of floats
        """
        if not self._is_initialized:
            self.initialize()
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * settings.vector_dimension
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents
        
        Args:
            texts: List of document texts
            
        Returns:
            List of embedding vectors
        """
        if not self._is_initialized:
            self.initialize()
        
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Return zero vectors as fallback
            return [[0.0] * settings.vector_dimension] * len(texts)


# Global instance
_embedder = None


def get_embedder() -> Embedder:
    """Get or create the global embedder instance"""
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
        _embedder.initialize()
    return _embedder
