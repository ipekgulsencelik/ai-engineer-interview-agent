import pytest

from src.domain.config.provider_config import ProviderConfig
from src.infrastructure.llm.mock_llm_client import MockLLMClient


def test_mock_llm_client_returns_response() -> None:
    client = MockLLMClient()

    assert client.generate("Hello") == "Mock LLM response."


def test_mock_llm_client_empty_prompt_raises_error() -> None:
    client = MockLLMClient()

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        client.generate("")


def test_mock_llm_client_accepts_provider_config() -> None:
    config = ProviderConfig(
        provider_name="mock",
        model_name="mock-test-model",
        temperature=0.1,
        max_tokens=256,
        timeout_seconds=10,
    )

    client = MockLLMClient(config=config)

    assert client.config.model_name == "mock-test-model"
    assert client.config.provider_name == "mock"
