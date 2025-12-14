"""Retriever component for RAG"""
import logging
from typing import List, Dict, Any, Optional

from app.rag.vector_db import get_default_vector_db

logger = logging.getLogger(__name__)


class Retriever:
    """Retrieves relevant documents for a given query"""
    
    def __init__(self, vector_db=None):
        """Initialize retriever
        
        Args:
            vector_db: Vector database instance (uses default if None)
        """
        self.vector_db = vector_db or get_default_vector_db()
        
    def retrieve(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant documents
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            filters: Optional metadata filters
            
        Returns:
            List of retrieved documents with scores
        """
        try:
            results = self.vector_db.search(query, top_k=top_k)
            
            # Apply metadata filters if provided
            if filters:
                results = self._apply_filters(results, filters)
            
            logger.info(f"Retrieved {len(results)} documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []
    
    def _apply_filters(self, results: List[Dict[str, Any]], filters: Dict) -> List[Dict[str, Any]]:
        """Apply metadata filters to results
        
        Args:
            results: Retrieved results
            filters: Filter criteria
            
        Returns:
            Filtered results
        """
        filtered = []
        for result in results:
            metadata = result.get("metadata", {})
            matches = all(
                metadata.get(key) == value 
                for key, value in filters.items()
            )
            if matches:
                filtered.append(result)
        
        return filtered
    
    def add_knowledge_base(self, documents: List[str], metadata: Optional[List[Dict]] = None):
        """Add documents to the knowledge base
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        try:
            self.vector_db.add_documents(documents, metadata)
            logger.info(f"Added {len(documents)} documents to knowledge base")
        except Exception as e:
            logger.error(f"Error adding documents to knowledge base: {e}")


# Global instance
_retriever = None


def get_retriever() -> Retriever:
    """Get or create the global retriever instance"""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
