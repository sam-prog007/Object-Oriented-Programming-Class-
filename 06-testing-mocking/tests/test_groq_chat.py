"""Mocking tests: the real Groq API is never called (no key, no cost, no network)."""

import os

import pytest

from src.groq_chat import MODEL, ask_groq


def test_ask_groq_returns_the_answer(fake_groq_client):
    assert ask_groq("What is 2+2?", client=fake_groq_client) == "4"


def test_ask_groq_calls_api_correctly(fake_groq_client):
    ask_groq("What is 2+2?", client=fake_groq_client)
    fake_groq_client.chat.completions.create.assert_called_once_with(
        model=MODEL,
        messages=[{"role": "user", "content": "What is 2+2?"}],
        max_tokens=1024,
    )


def test_ask_groq_raises_error_when_api_fails(mocker):
    client = mocker.Mock()
    client.chat.completions.create.side_effect = Exception("API down")   # simulated failure
    with pytest.raises(Exception, match="API down"):
        ask_groq("What is 2+2?", client=client)


@pytest.mark.parametrize("question", ["", "   ", "\n"])
def test_empty_question_never_reaches_the_api(question, fake_groq_client):
    with pytest.raises(ValueError, match="cannot be empty"):
        ask_groq(question, client=fake_groq_client)
    fake_groq_client.chat.completions.create.assert_not_called()


def test_default_client_is_created_when_none_given(mocker, fake_groq_client):
    """Patch the Groq class itself: ask_groq() without a client must build one."""
    groq_class = mocker.patch("src.groq_chat.Groq", return_value=fake_groq_client)
    assert ask_groq("Hello") == "4"
    groq_class.assert_called_once_with()


@pytest.mark.slow
@pytest.mark.skipif(not os.getenv("GROQ_API_KEY"), reason="needs a real GROQ_API_KEY")
def test_real_groq_api():
    """Calls the real API: slow and costs tokens, so it is marked and skipped by default."""
    answer = ask_groq("Reply with only the digit: what is 2+2?")
    assert "4" in answer
