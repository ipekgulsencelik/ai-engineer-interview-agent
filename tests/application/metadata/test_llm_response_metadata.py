import pytest

from src.application.metadata.llm_response_metadata import (
    LLMResponseMetadata,
)


def build_metadata(**overrides) -> LLMResponseMetadata:
    payload = {
        "model": "llama3-70b-8192",
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "total_tokens": 150,
        "latency_seconds": 1.25,
        "finish_reason": "stop",
        "raw_response": {"id": "abc"},
    }

    payload.update(overrides)

    return LLMResponseMetadata(**payload)


def test_llm_response_metadata_can_be_created() -> None:
    metadata = build_metadata()

    assert metadata.model == "llama3-70b-8192"
    assert metadata.prompt_tokens == 100
    assert metadata.completion_tokens == 50
    assert metadata.total_tokens == 150
    assert metadata.latency_seconds == 1.25
    assert metadata.finish_reason == "stop"

    assert metadata.raw_response == {
        "id": "abc",
    }


def test_llm_response_metadata_is_immutable() -> None:
    metadata = build_metadata()

    with pytest.raises(Exception):
        metadata.model = "gpt-4"


def test_llm_response_metadata_accepts_nullable_fields() -> None:
    metadata = LLMResponseMetadata()

    assert metadata.model is None
    assert metadata.prompt_tokens is None
    assert metadata.completion_tokens is None
    assert metadata.total_tokens is None
    assert metadata.latency_seconds is None
    assert metadata.finish_reason is None
    assert metadata.raw_response is None


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("prompt_tokens", -1),
        ("completion_tokens", -1),
        ("total_tokens", -1),
        ("latency_seconds", -0.1),
    ],
)
def test_llm_response_metadata_rejects_negative_numbers(
    field_name: str,
    value,
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    "value",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_llm_response_metadata_rejects_non_finite_latency(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            latency_seconds=value,
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("model", ""),
        ("model", "   "),
        ("finish_reason", ""),
        ("finish_reason", "   "),
    ],
)
def test_llm_response_metadata_rejects_empty_strings(
    field_name: str,
    value: str,
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("model", 123),
        ("prompt_tokens", "100"),
        ("completion_tokens", []),
        ("total_tokens", {}),
        ("latency_seconds", "fast"),
        ("finish_reason", 999),
        ("raw_response", "raw"),
    ],
)
def test_llm_response_metadata_rejects_invalid_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_metadata(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("prompt_tokens", True),
        ("completion_tokens", False),
        ("total_tokens", True),
        ("latency_seconds", False),
    ],
)
def test_llm_response_metadata_rejects_bool_numeric_values(
    field_name: str,
    value: bool,
) -> None:
    with pytest.raises(TypeError):
        build_metadata(
            **{
                field_name: value,
            }
        )