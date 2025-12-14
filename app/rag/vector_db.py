"""Vector database integration for RAG"""
import logging
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import numpy as np

logger = logging.getLogger(__name__)


class VectorDB(ABC):
    """Abstract base class for vector databases"""
    
    @abstractmethod
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> None:
        """Add documents to the vector database"""
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        pass
    
    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        """Delete documents by IDs"""
        pass


class FAISSVectorDB(VectorDB):
    """FAISS-based vector database implementation"""
    
    def __init__(self, dimension: int = 384):
        """Initialize FAISS vector database
        
        Args:
            dimension: Embedding dimension
        """
        self.dimension = dimension
        self.index = None
        self.documents = []
        self.metadata = []
        self._is_initialized = False
        
    def initialize(self):
        """Initialize FAISS index"""
        if self._is_initialized:
            return
            
        try:
            import faiss
            logger.info(f"Initializing FAISS index with dimension {self.dimension}")
            self.index = faiss.IndexFlatL2(self.dimension)
            self._is_initialized = True
            logger.info("FAISS index initialized successfully")
        except ImportError:
            logger.error("FAISS not installed. Install with: pip install faiss-cpu")
            raise
        except Exception as e:
            logger.error(f"Error initializing FAISS: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> None:
        """Add documents to FAISS index
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        if not self._is_initialized:
            self.initialize()
        
        from app.rag.embeddings import get_embedder
        embedder = get_embedder()
        
        # Generate embeddings
        embeddings = embedder.embed_documents(documents)
        
        # Add to index
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(documents)
        
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(documents))
        
        logger.info(f"Added {len(documents)} documents to FAISS index")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents
        
        Args:
            query: Query text
            top_k: Number of results to return
            
        Returns:
            List of result dictionaries
        """
        if not self._is_initialized or self.index.ntotal == 0:
            logger.warning("FAISS index not initialized or empty")
            return []
        
        from app.rag.embeddings import get_embedder
        embedder = get_embedder()
        
        # Generate query embedding
        query_embedding = embedder.embed_query(query)
        
        # Search
        distances, indices = self.index.search(
            np.array([query_embedding]).astype('float32'), 
            min(top_k, self.index.ntotal)
        )
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                results.append({
                    "document": self.documents[idx],
                    "score": float(dist),
                    "rank": i + 1,
                    "metadata": self.metadata[idx] if idx < len(self.metadata) else {}
                })
        
        logger.debug(f"Found {len(results)} similar documents")
        return results
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents by IDs (not implemented for basic FAISS)"""
        logger.warning("Delete operation not supported in basic FAISS implementation")
        pass


class ChromaVectorDB(VectorDB):
    """ChromaDB-based vector database implementation"""
    
    def __init__(self, collection_name: str = "chatbot_docs"):
        """Initialize ChromaDB
        
        Args:
            collection_name: Name of the collection
        """
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._is_initialized = False
        self._doc_counter = 0
        
    def initialize(self):
        """Initialize ChromaDB client"""
        if self._is_initialized:
            return
            
        try:
            import chromadb
            logger.info(f"Initializing ChromaDB collection: {self.collection_name}")
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            self._is_initialized = True
            logger.info("ChromaDB initialized successfully")
        except ImportError:
            logger.error("ChromaDB not installed. Install with: pip install chromadb")
            raise
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> None:
        """Add documents to ChromaDB
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        if not self._is_initialized:
            self.initialize()
        
        ids = [f"doc_{self._doc_counter + i}" for i in range(len(documents))]
        self._doc_counter += len(documents)
        
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadata if metadata else [{}] * len(documents)
        )
        
        logger.info(f"Added {len(documents)} documents to ChromaDB")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents
        
        Args:
            query: Query text
            top_k: Number of results to return
            
        Returns:
            List of result dictionaries
        """
        if not self._is_initialized:
            logger.warning("ChromaDB not initialized")
            return []
        
        results_obj = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        results = []
        if results_obj['documents'] and len(results_obj['documents']) > 0:
            for i, doc in enumerate(results_obj['documents'][0]):
                results.append({
                    "document": doc,
                    "score": results_obj['distances'][0][i] if results_obj['distances'] else 0,
                    "rank": i + 1,
                    "metadata": results_obj['metadatas'][0][i] if results_obj['metadatas'] else {}
                })
        
        logger.debug(f"Found {len(results)} similar documents")
        return results
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents by IDs
        
        Args:
            ids: List of document IDs to delete
        """
        if not self._is_initialized:
            return
        
        self.collection.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} documents from ChromaDB")


# Factory function
def get_vector_db(db_type: str = "faiss", **kwargs) -> VectorDB:
    """Factory function to create vector database instances
    
    Args:
        db_type: Type of vector database (faiss, chroma)
        **kwargs: Additional arguments for the database
        
    Returns:
        VectorDB instance
    """
    if db_type.lower() == "faiss":
        db = FAISSVectorDB(**kwargs)
        db.initialize()
        return db
    elif db_type.lower() == "chroma":
        db = ChromaVectorDB(**kwargs)
        db.initialize()
        return db
    else:
        raise ValueError(f"Unknown vector database type: {db_type}")


# Global instance
_vector_db = None


def get_default_vector_db() -> VectorDB:
    """Get or create the default vector database instance"""
    global _vector_db
    if _vector_db is None:
        from app.core.config import settings
        _vector_db = get_vector_db(
            db_type=settings.vector_db_type,
            dimension=settings.vector_dimension
        )
    return _vector_db
