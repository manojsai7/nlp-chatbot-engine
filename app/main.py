"""Main FastAPI application"""
import logging
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    Intent,
    Entity
)
from app.nlp.intent_classifier import get_intent_classifier
from app.nlp.entity_extractor import get_entity_extractor
from app.nlp.dialogue_manager import get_dialogue_manager
from app.memory.short_term import get_short_term_memory
from app.memory.long_term import get_long_term_memory
from app.middleware.safety import get_safety_filter
from app.middleware.rate_limit import get_rate_limiter
from app.evaluation.harness import get_evaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize NLP components
    try:
        get_intent_classifier()
        get_entity_extractor()
        logger.info("NLP components initialized")
    except Exception as e:
        logger.warning(f"Some NLP components failed to initialize: {e}")
    
    # Initialize memory
    try:
        get_short_term_memory()
        get_long_term_memory()
        logger.info("Memory components initialized")
    except Exception as e:
        logger.warning(f"Some memory components failed to initialize: {e}")


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """Main chat endpoint
    
    Args:
        request: Chat request payload
        req: FastAPI request object
        
    Returns:
        Chat response with intent, entities, and reply
    """
    try:
        # Rate limiting
        rate_limiter = get_rate_limiter()
        client_ip = req.client.host
        identifier = f"{request.user_id}:{client_ip}"
        
        if not rate_limiter.is_allowed(identifier):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Safety filter
        if settings.safety_filter_enabled:
            safety_filter = get_safety_filter()
            filter_result = safety_filter.filter_content(request.message)
            
            if not filter_result["is_safe"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Message content violates safety policies"
                )
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # NLP Processing
        intent_classifier = get_intent_classifier()
        entity_extractor = get_entity_extractor()
        dialogue_manager = get_dialogue_manager()
        
        # Classify intent
        intent_name, confidence = intent_classifier.classify(request.message)
        
        # Extract entities
        entities = entity_extractor.extract(request.message)
        
        # Get conversation history for context
        short_term_memory = get_short_term_memory()
        conversation_history = short_term_memory.get_conversation(session_id)
        
        # Generate response
        response_data = dialogue_manager.generate_response(
            intent=intent_name,
            confidence=confidence,
            entities=entities,
            context=request.context
        )
        
        # Store in memory
        short_term_memory.store_message(
            session_id=session_id,
            user_id=request.user_id,
            message=request.message,
            role="user"
        )
        
        short_term_memory.store_message(
            session_id=session_id,
            user_id=request.user_id,
            message=response_data["response"],
            role="assistant"
        )
        
        # Store in long-term memory if enabled
        if settings.long_term_memory_enabled:
            long_term_memory = get_long_term_memory()
            long_term_memory.store_conversation(
                session_id=session_id,
                user_id=request.user_id,
                message=request.message,
                intent=intent_name,
                confidence=confidence,
                response=response_data["response"]
            )
        
        # Prepare response
        chat_response = ChatResponse(
            response=response_data["response"],
            intent=Intent(
                name=intent_name,
                confidence=confidence,
                entities=[entity.model_dump() for entity in entities]
            ),
            entities=entities,
            session_id=session_id,
            confidence=confidence,
            suggestions=response_data.get("suggestions"),
            metadata=response_data.get("metadata")
        )
        
        logger.info(f"Processed chat request for user {request.user_id}, intent: {intent_name}")
        return chat_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your request"
        )


@app.get(f"{settings.api_prefix}/conversation/{{session_id}}")
async def get_conversation(session_id: str):
    """Get conversation history
    
    Args:
        session_id: Session identifier
        
    Returns:
        Conversation history
    """
    try:
        short_term_memory = get_short_term_memory()
        messages = short_term_memory.get_conversation(session_id)
        
        return {
            "session_id": session_id,
            "messages": messages,
            "message_count": len(messages)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversation history"
        )


@app.delete(f"{settings.api_prefix}/conversation/{{session_id}}")
async def clear_conversation(session_id: str):
    """Clear conversation history
    
    Args:
        session_id: Session identifier
        
    Returns:
        Success message
    """
    try:
        short_term_memory = get_short_term_memory()
        short_term_memory.clear_conversation(session_id)
        
        return {
            "message": "Conversation cleared successfully",
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error clearing conversation"
        )


@app.get(f"{settings.api_prefix}/user/{{user_id}}/history")
async def get_user_history(user_id: str, limit: int = 50):
    """Get user's conversation history from long-term memory
    
    Args:
        user_id: User identifier
        limit: Maximum number of records
        
    Returns:
        User conversation history
    """
    try:
        if not settings.long_term_memory_enabled:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Long-term memory is not enabled"
            )
        
        long_term_memory = get_long_term_memory()
        history = long_term_memory.get_user_history(user_id, limit)
        
        return {
            "user_id": user_id,
            "history": history,
            "count": len(history)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user history"
        )


@app.get(f"{settings.api_prefix}/evaluate")
async def run_evaluation():
    """Run evaluation harness on test conversations
    
    Returns:
        Evaluation results and metrics
    """
    try:
        evaluator = get_evaluator()
        results = evaluator.run_full_evaluation()
        
        return {
            "status": "completed",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error running evaluation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error running evaluation"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
