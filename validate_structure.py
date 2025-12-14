#!/usr/bin/env python3
"""
Simple validation script to test the chatbot engine structure
without requiring heavy dependencies like torch and spacy.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that core modules can be imported"""
    print("Testing core imports...")
    
    try:
        from app.core.config import settings
        print(f"✓ Configuration loaded: {settings.app_name} v{settings.app_version}")
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return False
    
    try:
        from app.core.models import ChatRequest, ChatResponse
        print("✓ Core models imported")
    except Exception as e:
        print(f"✗ Failed to import core models: {e}")
        return False
    
    return True


def test_adapters():
    """Test adapter imports"""
    print("\nTesting adapter imports...")
    
    try:
        from app.adapters.base import BaseAdapter
        from app.adapters.web import WebAdapter
        print("✓ Adapters imported")
        
        # Test web adapter instantiation
        web_adapter = WebAdapter()
        assert web_adapter.channel_name == "web"
        print("✓ Web adapter instantiated")
    except Exception as e:
        print(f"✗ Failed to test adapters: {e}")
        return False
    
    return True


def test_middleware():
    """Test middleware imports"""
    print("\nTesting middleware imports...")
    
    try:
        from app.middleware.safety import SafetyFilter
        from app.middleware.rate_limit import RateLimiter
        print("✓ Middleware imported")
        
        # Test safety filter
        safety_filter = SafetyFilter()
        assert safety_filter.is_safe("Hello, how are you?") == True
        assert safety_filter.is_safe("This is spam content") == False
        print("✓ Safety filter works")
        
        # Test rate limiter
        rate_limiter = RateLimiter(max_requests=5, time_window=60)
        assert rate_limiter.is_allowed("test_user") == True
        print("✓ Rate limiter works")
        
    except Exception as e:
        print(f"✗ Failed to test middleware: {e}")
        return False
    
    return True


def test_memory():
    """Test memory module imports"""
    print("\nTesting memory module imports...")
    
    try:
        from app.memory.summarizer import ConversationSummarizer
        print("✓ Memory modules imported")
        
        # Test summarizer
        summarizer = ConversationSummarizer(threshold=10)
        assert summarizer.should_summarize(5) == False
        assert summarizer.should_summarize(15) == True
        print("✓ Conversation summarizer works")
        
    except Exception as e:
        print(f"✗ Failed to test memory modules: {e}")
        return False
    
    return True


def test_dialogue_manager():
    """Test dialogue manager without NLP dependencies"""
    print("\nTesting dialogue manager...")
    
    try:
        from app.nlp.dialogue_manager import DialogueManager
        
        dm = DialogueManager()
        response = dm.generate_response(
            intent="greeting",
            confidence=0.85,
            entities=None,
            context=None
        )
        
        assert "response" in response
        assert response["confidence"] == 0.85
        print(f"✓ Dialogue manager works")
        print(f"  Sample response: {response['response'][:50]}...")
        
    except Exception as e:
        print(f"✗ Failed to test dialogue manager: {e}")
        return False
    
    return True


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("NLP Chatbot Engine - Structure Validation")
    print("=" * 60)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_adapters()
    all_passed &= test_middleware()
    all_passed &= test_memory()
    all_passed &= test_dialogue_manager()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All validation tests passed!")
        print("\nNOTE: To run the full application, install all dependencies:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")
        print("=" * 60)
        return 0
    else:
        print("✗ Some validation tests failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
