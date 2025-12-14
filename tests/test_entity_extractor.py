"""Tests for entity extractor"""
import pytest
from app.nlp.entity_extractor import EntityExtractor


def test_entity_extractor_initialization():
    """Test entity extractor can be initialized"""
    extractor = EntityExtractor()
    assert extractor is not None


def test_email_extraction():
    """Test email entity extraction (rule-based fallback)"""
    extractor = EntityExtractor()
    entities = extractor.extract("My email is john@example.com")
    
    # Check if any email entity was found
    email_entities = [e for e in entities if e.label == "EMAIL"]
    assert len(email_entities) >= 1
    assert "john@example.com" in email_entities[0].text


def test_phone_extraction():
    """Test phone number extraction (rule-based fallback)"""
    extractor = EntityExtractor()
    entities = extractor.extract("Call me at 555-123-4567")
    
    # Check if any phone entity was found
    phone_entities = [e for e in entities if e.label == "PHONE"]
    assert len(phone_entities) >= 1


def test_extract_with_context():
    """Test extraction with context"""
    extractor = EntityExtractor()
    result = extractor.extract_with_context("Email me at test@example.com")
    
    assert "entities" in result
    assert "entity_count" in result
    assert "entity_types" in result
    assert isinstance(result["entities"], list)
