"""Basic example of using the NLP Chatbot Engine."""
from nlp_chatbot_engine import ChatbotEngine, IntentClassifier, EntityExtractor, ContextManager


def main():
    # Initialize the engine
    engine = ChatbotEngine()
    
    # Configure intents
    engine.intent_classifier.add_intent(
        "greeting",
        keywords=["hello", "hi", "hey", "greetings"],
        patterns=[r"^(hello|hi|hey)"]
    )
    
    engine.intent_classifier.add_intent(
        "farewell",
        keywords=["bye", "goodbye", "see you", "farewell"],
        patterns=[r"(bye|goodbye)"]
    )
    
    engine.intent_classifier.add_intent(
        "order_pizza",
        keywords=["pizza", "order", "delivery"],
        patterns=[r"(order|want|get).*pizza"]
    )
    
    # Register intent handlers
    def handle_greeting(message, entities, context):
        return "Hello! How can I help you today?"
    
    def handle_farewell(message, entities, context):
        return "Goodbye! Have a great day!"
    
    def handle_pizza_order(message, entities, context):
        return "I'd be happy to help you order a pizza! What size would you like?"
    
    engine.register_intent_handler("greeting", handle_greeting)
    engine.register_intent_handler("farewell", handle_farewell)
    engine.register_intent_handler("order_pizza", handle_pizza_order)
    
    # Process some messages
    user_id = "user123"
    
    messages = [
        "Hello there!",
        "I want to order a pizza",
        "My email is test@example.com",
        "Goodbye!",
    ]
    
    print("=" * 60)
    print("NLP Chatbot Engine - Basic Example")
    print("=" * 60)
    
    for message in messages:
        print(f"\nUser: {message}")
        result = engine.process_message(message, user_id)
        
        print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        
        if result['entities']:
            print(f"Entities: {result['entities']}")
        
        if 'response' in result:
            print(f"Bot: {result['response']}")


if __name__ == "__main__":
    main()
