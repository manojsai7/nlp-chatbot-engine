#!/usr/bin/env python3
"""
Example usage of the NLP Chatbot Engine.

This script demonstrates basic usage patterns without requiring
full installation of ML libraries.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.models import ChatRequest
from app.nlp.dialogue_manager import DialogueManager
from app.middleware.safety import SafetyFilter
from app.middleware.rate_limit import RateLimiter
from app.adapters.web import WebAdapter


def example_basic_conversation():
    """Example: Basic conversation flow"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Conversation")
    print("=" * 60)
    
    dialogue_manager = DialogueManager()
    
    # Simulate a conversation
    conversations = [
        ("Hello!", "greeting"),
        ("I need help with something", "help"),
        ("What is the weather like?", "question"),
        ("Thank you, goodbye!", "farewell")
    ]
    
    for message, expected_intent in conversations:
        print(f"\nUser: {message}")
        
        # Generate response
        response = dialogue_manager.generate_response(
            intent=expected_intent,
            confidence=0.85,
            entities=None
        )
        
        print(f"Bot: {response['response']}")
        if response.get('suggestions'):
            print(f"Suggestions: {', '.join(response['suggestions'][:2])}")


def example_safety_filter():
    """Example: Content safety filtering"""
    print("\n" + "=" * 60)
    print("Example 2: Safety Filtering")
    print("=" * 60)
    
    safety_filter = SafetyFilter()
    
    test_messages = [
        "Hello, how can you help me?",
        "This is a spam message",
        "My credit card number is 1234",
        "I want to abuse the system"
    ]
    
    for message in test_messages:
        is_safe = safety_filter.is_safe(message)
        status = "✓ SAFE" if is_safe else "✗ BLOCKED"
        print(f"{status}: {message}")


def example_rate_limiting():
    """Example: Rate limiting"""
    print("\n" + "=" * 60)
    print("Example 3: Rate Limiting")
    print("=" * 60)
    
    rate_limiter = RateLimiter(max_requests=3, time_window=60)
    user_id = "test_user_123"
    
    print(f"Rate limit: 3 requests per 60 seconds\n")
    
    for i in range(5):
        is_allowed = rate_limiter.is_allowed(user_id)
        remaining = rate_limiter.get_remaining_requests(user_id)
        
        status = "✓ ALLOWED" if is_allowed else "✗ BLOCKED"
        print(f"Request {i+1}: {status} (Remaining: {remaining})")


def example_channel_adapter():
    """Example: Using channel adapters"""
    print("\n" + "=" * 60)
    print("Example 4: Channel Adapters")
    print("=" * 60)
    
    import asyncio
    
    async def test_adapter():
        web_adapter = WebAdapter()
        
        # Simulate receiving a message
        incoming_payload = {
            "message": "Hello from web client",
            "user_id": "user123",
            "session_id": "session456"
        }
        
        normalized = await web_adapter.receive_message(incoming_payload)
        print(f"Received message: {normalized['text']}")
        print(f"Channel: {normalized['channel']}")
        print(f"User ID: {normalized['user_id']}")
        
        # Simulate sending a response
        success = await web_adapter.send_message(
            recipient="user123",
            message="Hello! How can I help you?"
        )
        print(f"\nResponse sent: {'✓' if success else '✗'}")
    
    asyncio.run(test_adapter())


def example_dialogue_with_context():
    """Example: Context-aware dialogue"""
    print("\n" + "=" * 60)
    print("Example 5: Context-Aware Dialogue")
    print("=" * 60)
    
    dialogue_manager = DialogueManager()
    
    # Simulate conversation with history
    conversation_history = [
        {"intent": "greeting", "content": "Hello"},
        {"intent": "question", "content": "What is your name?"},
    ]
    
    current_intent = "question"
    
    context = dialogue_manager.manage_context(
        current_intent=current_intent,
        conversation_history=conversation_history
    )
    
    print(f"Conversation turns: {context['turn_count']}")
    print(f"Recent intents: {context['recent_intents']}")
    print(f"Is follow-up: {context['is_follow_up']}")
    
    # Generate response with context
    response = dialogue_manager.generate_response(
        intent=current_intent,
        confidence=0.90,
        entities=None,
        context=context
    )
    
    print(f"\nGenerated response: {response['response']}")


def main():
    """Run all examples"""
    print("=" * 60)
    print("NLP Chatbot Engine - Usage Examples")
    print("=" * 60)
    
    try:
        example_basic_conversation()
        example_safety_filter()
        example_rate_limiting()
        example_channel_adapter()
        example_dialogue_with_context()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("\nTo use with full NLP capabilities:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Download spaCy model: python -m spacy download en_core_web_sm")
        print("  3. Start the API: uvicorn app.main:app --reload")
        print("  4. Visit: http://localhost:8000/docs")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
