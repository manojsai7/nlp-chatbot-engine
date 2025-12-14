"""Example showing context and memory management."""
from nlp_chatbot_engine import ChatbotEngine


def main():
    # Initialize engine
    engine = ChatbotEngine()
    
    # Configure intents
    engine.intent_classifier.add_intent(
        "book_hotel",
        keywords=["book", "hotel", "room", "reservation"],
    )
    
    engine.intent_classifier.add_intent(
        "confirm",
        keywords=["yes", "confirm", "correct", "okay"],
    )
    
    # Handler that uses context
    def handle_book_hotel(message, entities, context):
        # Extract location from entities
        locations = [e['value'] for e in entities if e['type'] == 'location']
        
        if locations:
            return f"Great! I'll help you book a hotel in {locations[0]}. Can you confirm?"
        else:
            return "Where would you like to book a hotel?"
    
    def handle_confirm(message, entities, context):
        last_intent = context.get("last_intent")
        
        if last_intent == "book_hotel":
            return "Perfect! Your hotel booking has been confirmed."
        else:
            return "What would you like me to confirm?"
    
    engine.register_intent_handler("book_hotel", handle_book_hotel)
    engine.register_intent_handler("confirm", handle_confirm)
    
    # Add custom entity extractor for locations (simple example)
    def extract_cities(text):
        cities = ["New York", "London", "Paris", "Tokyo", "Sydney"]
        found = []
        for city in cities:
            if city.lower() in text.lower():
                found.append({"value": city, "type": "location"})
        return found
    
    engine.entity_extractor.add_custom_extractor("location", extract_cities)
    
    print("=" * 60)
    print("NLP Chatbot Engine - Context Management Example")
    print("=" * 60)
    
    user_id = "user_context_demo"
    
    # Conversation with context
    messages = [
        "I want to book a hotel in Paris",
        "Yes, that's correct",
    ]
    
    for message in messages:
        print(f"\nUser: {message}")
        result = engine.process_message(message, user_id)
        
        print(f"Intent: {result['intent']}")
        
        if result['entities']:
            print(f"Entities: {[e['value'] for e in result['entities']]}")
        
        if 'response' in result:
            print(f"Bot: {result['response']}")
    
    # Show context
    context = engine.context_manager.get_context(user_id)
    print(f"\nFinal Context: {context}")


if __name__ == "__main__":
    main()
