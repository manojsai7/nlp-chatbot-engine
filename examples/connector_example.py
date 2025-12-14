"""Example demonstrating multi-channel connectors."""
from nlp_chatbot_engine import ChatbotEngine
from nlp_chatbot_engine.connectors.web_connector import WebConnector


def main():
    # Initialize the engine
    engine = ChatbotEngine()
    
    # Configure intents
    engine.intent_classifier.add_intent(
        "help",
        keywords=["help", "support", "assist"],
    )
    
    engine.intent_classifier.add_intent(
        "status",
        keywords=["status", "check", "how"],
    )
    
    # Register handlers
    def handle_help(message, entities, context):
        return "I can help you with various tasks. Just ask!"
    
    def handle_status(message, entities, context):
        return "All systems are operational!"
    
    engine.register_intent_handler("help", handle_help)
    engine.register_intent_handler("status", handle_status)
    
    # Create web connector
    web_connector = WebConnector(engine)
    web_connector.connect()
    
    print("=" * 60)
    print("NLP Chatbot Engine - Web Connector Example")
    print("=" * 60)
    
    # Simulate web requests
    requests = [
        ("user1", "I need help"),
        ("user2", "What's the status?"),
        ("user1", "Contact me at support@example.com"),
    ]
    
    for user_id, message in requests:
        print(f"\n[{user_id}] Request: {message}")
        response = web_connector.handle_request(user_id, message)
        print(f"[{user_id}] Response: {response['response']}")
        print(f"[{user_id}] Intent: {response['intent']} ({response['confidence']:.2f})")
    
    web_connector.disconnect()


if __name__ == "__main__":
    main()
