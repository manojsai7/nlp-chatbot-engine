"""Tests for EntityExtractor."""
import pytest
from nlp_chatbot_engine.entities.entity_extractor import EntityExtractor


def test_entity_extractor_initialization():
    """Test extractor initializes with default patterns."""
    extractor = EntityExtractor()
    assert "email" in extractor.patterns
    assert "phone" in extractor.patterns
    assert "url" in extractor.patterns


def test_extract_email():
    """Test email extraction."""
    extractor = EntityExtractor()
    entities = extractor.extract("Contact me at test@example.com")
    
    emails = [e for e in entities if e["type"] == "email"]
    assert len(emails) == 1
    assert emails[0]["value"] == "test@example.com"


def test_extract_phone():
    """Test phone number extraction."""
    extractor = EntityExtractor()
    entities = extractor.extract("Call me at 555-123-4567")
    
    phones = [e for e in entities if e["type"] == "phone"]
    assert len(phones) == 1


def test_extract_url():
    """Test URL extraction."""
    extractor = EntityExtractor()
    entities = extractor.extract("Visit https://example.com for more")
    
    urls = [e for e in entities if e["type"] == "url"]
    assert len(urls) == 1
    assert "example.com" in urls[0]["value"]


def test_extract_number():
    """Test number extraction."""
    extractor = EntityExtractor()
    entities = extractor.extract("I need 5 pizzas")
    
    numbers = [e for e in entities if e["type"] == "number"]
    assert len(numbers) == 1
    assert numbers[0]["value"] == "5"


def test_add_pattern():
    """Test adding custom patterns."""
    extractor = EntityExtractor()
    extractor.add_pattern("custom", r"\btest\b")
    
    entities = extractor.extract("this is a test message")
    customs = [e for e in entities if e["type"] == "custom"]
    assert len(customs) == 1


def test_add_custom_extractor():
    """Test adding custom extractor function."""
    extractor = EntityExtractor()
    
    def extract_currency(text):
        return [{"value": "$100"}] if "$" in text else []
    
    extractor.add_custom_extractor("currency", extract_currency)
    
    entities = extractor.extract("Price is $100")
    currencies = [e for e in entities if e["type"] == "currency"]
    assert len(currencies) == 1


def test_extract_by_type():
    """Test extracting entities by type."""
    extractor = EntityExtractor()
    text = "Email me at test@example.com or call 555-1234"
    
    emails = extractor.extract_by_type(text, "email")
    assert len(emails) == 1
    assert emails[0] == "test@example.com"


def test_has_entity_type():
    """Test checking for entity type."""
    extractor = EntityExtractor()
    
    assert extractor.has_entity_type("Email: test@example.com", "email")
    assert not extractor.has_entity_type("No email here", "email")


def test_entity_positions():
    """Test entity position tracking."""
    extractor = EntityExtractor()
    entities = extractor.extract("Email test@example.com here")
    
    email = [e for e in entities if e["type"] == "email"][0]
    assert "start" in email
    assert "end" in email
    assert email["start"] < email["end"]


def test_multiple_entities():
    """Test extracting multiple entities."""
    extractor = EntityExtractor()
    text = "Contact test@example.com or call 555-123-4567 or visit https://example.com"
    
    entities = extractor.extract(text)
    
    # Should have email, phone, and url
    types = {e["type"] for e in entities}
    assert "email" in types
    assert "phone" in types
    assert "url" in types
