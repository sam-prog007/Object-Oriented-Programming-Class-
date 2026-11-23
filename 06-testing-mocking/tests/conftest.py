"""Fixtures shared by every test file (pytest finds this file automatically)."""

import pytest

from src.app import OrderService, ProductRepository


@pytest.fixture
def repo():
    """A fresh repository for each test, so tests never affect each other."""
    return ProductRepository()


@pytest.fixture
def order_service(repo):
    return OrderService(repo)


@pytest.fixture
def fake_groq_client(mocker):
    """A fake Groq client whose create() returns an answer of "4"."""
    mock_choice = mocker.Mock()
    mock_choice.message.content = "4"
    mock_response = mocker.Mock()
    mock_response.choices = [mock_choice]
    client = mocker.Mock()
    client.chat.completions.create.return_value = mock_response
    return client
