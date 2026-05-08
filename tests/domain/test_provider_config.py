import pytest

from src.domain.config.provider_config import ProviderConfig


def test_provider_config_can_be_created_with_valid_data() -> None:
    config = ProviderConfig(
        provider_name="groq",
        model_name="llama3-70b-8192",
        temperature=0.2,
        max_tokens=1024,
        timeout_seconds=30,
    )

    assert config.provider_name == "groq"
    assert config.model_name == "llama3-70b-8192"
    assert config.temperature == 0.2
    assert config.max_tokens == 1024
    assert config.timeout_seconds == 30


def test_provider_config_empty_provider_name_raises_error() -> None:
    with pytest.raises(ValueError, match="Provider name cannot be empty"):
        ProviderConfig(
            provider_name="",
            model_name="llama3-70b-8192",
        )


def test_provider_config_empty_model_name_raises_error() -> None:
    with pytest.raises(ValueError, match="Model name cannot be empty"):
        ProviderConfig(
            provider_name="groq",
            model_name="",
        )


def test_provider_config_invalid_temperature_raises_error() -> None:
    with pytest.raises(ValueError, match="Temperature must be between 0 and 2"):
        ProviderConfig(
            provider_name="groq",
            model_name="llama3-70b-8192",
            temperature=3,
        )


def test_provider_config_invalid_max_tokens_raises_error() -> None:
    with pytest.raises(ValueError, match="Max tokens must be greater than 0"):
        ProviderConfig(
            provider_name="groq",
            model_name="llama3-70b-8192",
            max_tokens=0,
        )


def test_provider_config_invalid_timeout_raises_error() -> None:
    with pytest.raises(ValueError, match="Timeout seconds must be greater than 0"):
        ProviderConfig(
            provider_name="groq",
            model_name="llama3-70b-8192",
            timeout_seconds=0,
        )
