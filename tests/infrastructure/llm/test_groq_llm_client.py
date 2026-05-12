from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.application.models.llm_request import LLMRequest
from src.application.models.llm_response import LLMResponse
from src.infrastructure.llm.groq_llm_client import GroqLLMClient


class FakeGroqCompletions:
    def __init__(
        self,
        response: object,
    ) -> None:
        self._response = response
        self.called_with: dict | None = None

    def create(
        self,
        **kwargs,
    ) -> object:
        self.called_with = kwargs
        return self._response


class FakeGroqClient:
    def __init__(
        self,
        response: object,
    ) -> None:
        self.completions = FakeGroqCompletions(response)
        self.chat = SimpleNamespace(
            completions=self.completions,
        )


def build_groq_response(
    *,
    content: str | None = '{"score": 8}',
    prompt_tokens: int | None = 10,
    completion_tokens: int | None = 32,
    total_tokens: int | None = 42,
    finish_reason: str | None = "stop",
) -> object:
    usage = None

    if (
        prompt_tokens is not None
        or completion_tokens is not None
        or total_tokens is not None
    ):
        usage = SimpleNamespace(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )

    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=content,
                ),
                finish_reason=finish_reason,
            ),
        ],
        usage=usage,
    )


def build_client(
    response: object,
) -> tuple[GroqLLMClient, FakeGroqClient]:
    fake_client = FakeGroqClient(response)

    client = GroqLLMClient(
        api_key="test-api-key",
        model_name="llama3-70b-8192",
        client=fake_client,
    )

    return client, fake_client


def test_generate_returns_llm_response() -> None:
    response = build_groq_response(
        content='{"score": 8}',
        prompt_tokens=10,
        completion_tokens=32,
        total_tokens=42,
        finish_reason="stop",
    )

    client, _ = build_client(response)

    result = client.generate(
        LLMRequest(
            prompt="Evaluate this answer.",
            temperature=0.0,
        ),
    )

    assert isinstance(result, LLMResponse)
    assert result.text == '{"score": 8}'
    assert result.metadata.model == "llama3-70b-8192"
    assert result.metadata.prompt_tokens == 10
    assert result.metadata.completion_tokens == 32
    assert result.metadata.total_tokens == 42
    assert result.metadata.finish_reason == "stop"
    assert result.metadata.latency_seconds is not None
    assert result.metadata.latency_seconds >= 0.0


def test_generate_calls_groq_with_expected_arguments() -> None:
    response = build_groq_response()

    client, fake_client = build_client(response)

    client.generate(
        LLMRequest(
            prompt="Prompt text",
            temperature=0.2,
        ),
    )

    assert fake_client.completions.called_with == {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": "Prompt text",
            },
        ],
        "temperature": 0.2,
        "max_tokens": None,
        "stop": None,
    }


def test_generate_includes_system_prompt_when_present() -> None:
    response = build_groq_response()

    client, fake_client = build_client(response)

    client.generate(
        LLMRequest(
            system_prompt="You are strict.",
            prompt="Return JSON only.",
            temperature=0.0,
        ),
    )

    assert fake_client.completions.called_with == {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are strict.",
            },
            {
                "role": "user",
                "content": "Return JSON only.",
            },
        ],
        "temperature": 0.0,
        "max_tokens": None,
        "stop": None,
    }


def test_generate_passes_max_tokens_and_stop() -> None:
    response = build_groq_response()

    client, fake_client = build_client(response)

    client.generate(
        LLMRequest(
            prompt="Prompt text",
            temperature=0.0,
            max_tokens=256,
            stop=("END",),
        ),
    )

    assert fake_client.completions.called_with == {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": "Prompt text",
            },
        ],
        "temperature": 0.0,
        "max_tokens": 256,
        "stop": ("END",),
    }


@pytest.mark.parametrize(
    "prompt",
    [
        "",
        "   ",
    ],
)
def test_llm_request_rejects_empty_prompt(
    prompt: str,
) -> None:
    with pytest.raises(ValueError):
        LLMRequest(
            prompt=prompt,
        )


def test_generate_rejects_non_llm_request() -> None:
    response = build_groq_response()

    client, _ = build_client(response)

    with pytest.raises(
        TypeError,
        match="request must be an LLMRequest",
    ):
        client.generate("Prompt text")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "api_key",
    [
        "",
        "   ",
    ],
)
def test_constructor_rejects_empty_api_key(
    api_key: str,
) -> None:
    response = build_groq_response()
    fake_client = FakeGroqClient(response)

    with pytest.raises(ValueError):
        GroqLLMClient(
            api_key=api_key,
            model_name="llama3-70b-8192",
            client=fake_client,
        )


def test_constructor_rejects_non_string_api_key() -> None:
    response = build_groq_response()
    fake_client = FakeGroqClient(response)

    with pytest.raises(TypeError):
        GroqLLMClient(
            api_key=123,  # type: ignore[arg-type]
            model_name="llama3-70b-8192",
            client=fake_client,
        )


@pytest.mark.parametrize(
    "model_name",
    [
        "",
        "   ",
    ],
)
def test_constructor_rejects_empty_model_name(
    model_name: str,
) -> None:
    response = build_groq_response()
    fake_client = FakeGroqClient(response)

    with pytest.raises(ValueError):
        GroqLLMClient(
            api_key="test-api-key",
            model_name=model_name,
            client=fake_client,
        )


def test_constructor_rejects_non_string_model_name() -> None:
    response = build_groq_response()
    fake_client = FakeGroqClient(response)

    with pytest.raises(TypeError):
        GroqLLMClient(
            api_key="test-api-key",
            model_name=123,  # type: ignore[arg-type]
            client=fake_client,
        )


@pytest.mark.parametrize(
    "temperature",
    [
        -0.1,
        2.1,
        float("inf"),
        float("nan"),
    ],
)
def test_llm_request_rejects_invalid_temperature(
    temperature: float,
) -> None:
    with pytest.raises(ValueError):
        LLMRequest(
            prompt="Prompt text",
            temperature=temperature,
        )


def test_llm_request_rejects_boolean_temperature() -> None:
    with pytest.raises(TypeError):
        LLMRequest(
            prompt="Prompt text",
            temperature=True,  # type: ignore[arg-type]
        )


def test_generate_raises_when_choices_missing() -> None:
    response = SimpleNamespace(
        choices=[],
        usage=None,
    )

    client, _ = build_client(response)

    with pytest.raises(
        ValueError,
        match="choices cannot be empty",
    ):
        client.generate(
            LLMRequest(
                prompt="Prompt text",
            ),
        )


def test_generate_raises_when_message_missing() -> None:
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=None,
            ),
        ],
        usage=None,
    )

    client, _ = build_client(response)

    with pytest.raises(
        ValueError,
        match="message cannot be None",
    ):
        client.generate(
            LLMRequest(
                prompt="Prompt text",
            ),
        )


def test_generate_raises_when_content_missing() -> None:
    response = build_groq_response(
        content=None,
    )

    client, _ = build_client(response)

    with pytest.raises(
        ValueError,
        match="content cannot be None",
    ):
        client.generate(
            LLMRequest(
                prompt="Prompt text",
            ),
        )


def test_generate_raises_when_content_empty() -> None:
    response = build_groq_response(
        content="   ",
    )

    client, _ = build_client(response)

    with pytest.raises(
        ValueError,
        match="content cannot be empty",
    ):
        client.generate(
            LLMRequest(
                prompt="Prompt text",
            ),
        )


def test_generate_returns_none_token_metadata_when_usage_missing() -> None:
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content='{"score": 7}',
                ),
                finish_reason="stop",
            ),
        ],
        usage=None,
    )

    client, _ = build_client(response)

    result = client.generate(
        LLMRequest(
            prompt="Prompt text",
        ),
    )

    assert result.metadata.prompt_tokens is None
    assert result.metadata.completion_tokens is None
    assert result.metadata.total_tokens is None
    assert result.metadata.finish_reason == "stop"


def test_generate_returns_none_finish_reason_when_missing() -> None:
    response = build_groq_response(
        finish_reason=None,
    )

    client, _ = build_client(response)

    result = client.generate(
        LLMRequest(
            prompt="Prompt text",
        ),
    )

    assert result.metadata.finish_reason is None