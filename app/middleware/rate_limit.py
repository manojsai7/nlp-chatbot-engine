"""Rate limiting middleware"""
import logging
import time
from typing import Dict, Optional
from collections import defaultdict, deque

from app.core.config import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiting for API requests"""
    
    def __init__(
        self,
        max_requests: int = None,
        time_window: int = None,
        use_redis: bool = False
    ):
        """Initialize rate limiter
        
        Args:
            max_requests: Maximum requests per time window
            time_window: Time window in seconds
            use_redis: Use Redis for distributed rate limiting
        """
        self.max_requests = max_requests or settings.rate_limit_requests
        self.time_window = time_window or settings.rate_limit_period
        self.use_redis = use_redis
        
        # In-memory storage (for single instance)
        self._requests: Dict[str, deque] = defaultdict(deque)
        
        # Redis client (for distributed)
        self.redis_client = None
        if use_redis:
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis client for distributed rate limiting"""
        try:
            import redis
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("Redis initialized for rate limiting")
        except Exception as e:
            logger.warning(f"Redis not available for rate limiting: {e}")
            self.redis_client = None
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed
        
        Args:
            identifier: User/IP identifier
            
        Returns:
            True if request is allowed
        """
        if not settings.rate_limit_enabled:
            return True
        
        if self.redis_client:
            return self._is_allowed_redis(identifier)
        else:
            return self._is_allowed_memory(identifier)
    
    def _is_allowed_memory(self, identifier: str) -> bool:
        """In-memory rate limiting check
        
        Args:
            identifier: User/IP identifier
            
        Returns:
            True if allowed
        """
        current_time = time.time()
        cutoff_time = current_time - self.time_window
        
        # Clean old requests
        requests = self._requests[identifier]
        while requests and requests[0] < cutoff_time:
            requests.popleft()
        
        # Check limit
        if len(requests) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False
        
        # Add current request
        requests.append(current_time)
        return True
    
    def _is_allowed_redis(self, identifier: str) -> bool:
        """Redis-based rate limiting check
        
        Args:
            identifier: User/IP identifier
            
        Returns:
            True if allowed
        """
        try:
            key = f"ratelimit:{identifier}"
            current_time = time.time()
            
            # Use sorted set to track requests
            pipe = self.redis_client.pipeline()
            
            # Remove old requests
            cutoff = current_time - self.time_window
            pipe.zremrangebyscore(key, 0, cutoff)
            
            # Count requests in window
            pipe.zcard(key)
            
            # Add current request
            pipe.zadd(key, {str(current_time): current_time})
            
            # Set expiry
            pipe.expire(key, self.time_window)
            
            results = pipe.execute()
            request_count = results[1]
            
            if request_count >= self.max_requests:
                logger.warning(f"Rate limit exceeded for {identifier}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in Redis rate limiting: {e}")
            # Fail open - allow request if Redis fails
            return True
    
    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier
        
        Args:
            identifier: User/IP identifier
            
        Returns:
            Number of remaining requests
        """
        if not settings.rate_limit_enabled:
            return self.max_requests
        
        if self.redis_client:
            return self._get_remaining_redis(identifier)
        else:
            return self._get_remaining_memory(identifier)
    
    def _get_remaining_memory(self, identifier: str) -> int:
        """Get remaining requests (in-memory)"""
        current_time = time.time()
        cutoff_time = current_time - self.time_window
        
        requests = self._requests[identifier]
        # Count requests in window
        valid_requests = sum(1 for req_time in requests if req_time > cutoff_time)
        
        return max(0, self.max_requests - valid_requests)
    
    def _get_remaining_redis(self, identifier: str) -> int:
        """Get remaining requests (Redis)"""
        try:
            key = f"ratelimit:{identifier}"
            current_time = time.time()
            cutoff = current_time - self.time_window
            
            # Remove old and count
            pipe = self.redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, cutoff)
            pipe.zcard(key)
            results = pipe.execute()
            
            request_count = results[1]
            return max(0, self.max_requests - request_count)
            
        except Exception as e:
            logger.error(f"Error getting remaining requests: {e}")
            return self.max_requests


# Global instance
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get or create the global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
