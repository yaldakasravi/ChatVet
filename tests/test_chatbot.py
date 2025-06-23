# tests/test_chatbot.py

import pytest
from chatbot import Chatbot

# Instantiate chatbot once for testing
chatbot = Chatbot()

def test_valid_symptom_query():
    """Test a normal user query about a pet symptom."""
    question = "My dog has diarrhea and won’t eat."
    response = chatbot.ask(question)
    assert isinstance(response, str)
    assert len(response) > 20
    assert "consult" in response.lower() or "vet" in response.lower()


def test_gibberish_input():
    """Test how the chatbot handles nonsense input."""
    question = "asdjlkajsdlkajsd qwoieurioweur"
    response = chatbot.ask(question)
    assert isinstance(response, str)
    assert "please ask" in response.lower() or len(response) > 5


def test_empty_input():
    """Test response to an empty string input."""
    response = chatbot.ask("")
    assert response.lower().startswith("please ask a valid")


def test_short_input():
    """Test very short but real input."""
    response = chatbot.ask("Vomiting")
    assert isinstance(response, str)
    assert len(response) > 10


def test_symptom_checker_first():
    """Force a known match to check the symptom checker kicks in."""
    response = chatbot.ask("My puppy has worms in her stool")
    assert "deworming" in response.lower() or "puppies" in response.lower()


@pytest.mark.skip(reason="Optional: stress test with long input")
def test_long_input():
    question = "My cat has been sneezing, has watery eyes, and seems a bit off. " * 10
    response = chatbot.ask(question)
    assert isinstance(response, str)
    assert len(response) > 30
