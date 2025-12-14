"""Tests for connectors."""
import pytest
from nlp_chatbot_engine import ChatbotEngine
from nlp_chatbot_engine.connectors.web_connector import WebConnector
from nlp_chatbot_engine.connectors.slack_connector import SlackConnector
from nlp_chatbot_engine.connectors.discord_connector import DiscordConnector


def test_web_connector_initialization():
    """Test web connector initializes correctly."""
    engine = ChatbotEngine()
    connector = WebConnector(engine)
    
    assert connector.engine is engine
    assert not connector.is_connected()


def test_web_connector_connect():
    """Test web connector connection."""
    engine = ChatbotEngine()
    connector = WebConnector(engine)
    
    connector.connect()
    assert connector.is_connected()


def test_web_connector_handle_request():
    """Test handling web requests."""
    engine = ChatbotEngine()
    engine.intent_classifier.add_intent("greeting", keywords=["hello"])
    
    def handle_greeting(message, entities, context):
        return "Hi there!"
    
    engine.register_intent_handler("greeting", handle_greeting)
    
    connector = WebConnector(engine)
    connector.connect()
    
    response = connector.handle_request("user1", "hello")
    
    assert response["success"] is True
    assert "response" in response
    assert response["intent"] == "greeting"


def test_slack_connector_initialization():
    """Test Slack connector initializes correctly."""
    engine = ChatbotEngine()
    config = {"bot_token": "test_token"}
    connector = SlackConnector(engine, config)
    
    assert connector.bot_token == "test_token"
    assert not connector.is_connected()


def test_slack_connector_requires_token():
    """Test Slack connector requires token."""
    engine = ChatbotEngine()
    connector = SlackConnector(engine)
    
    with pytest.raises(ValueError):
        connector.connect()


def test_discord_connector_initialization():
    """Test Discord connector initializes correctly."""
    engine = ChatbotEngine()
    config = {"bot_token": "test_token"}
    connector = DiscordConnector(engine, config)
    
    assert connector.bot_token == "test_token"
    assert not connector.is_connected()


def test_discord_connector_requires_token():
    """Test Discord connector requires token."""
    engine = ChatbotEngine()
    connector = DiscordConnector(engine)
    
    with pytest.raises(ValueError):
        connector.connect()


def test_connector_process_incoming_message():
    """Test processing incoming messages."""
    engine = ChatbotEngine()
    engine.intent_classifier.add_intent("test", keywords=["test"])
    
    connector = WebConnector(engine)
    
    result = connector.process_incoming_message({
        "user_id": "user1",
        "message": "test message"
    })
    
    assert "intent" in result
    assert result["message"] == "test message"


def test_connector_disconnect():
    """Test connector disconnection."""
    engine = ChatbotEngine()
    connector = WebConnector(engine)
    
    connector.connect()
    assert connector.is_connected()
    
    connector.disconnect()
    assert not connector.is_connected()
