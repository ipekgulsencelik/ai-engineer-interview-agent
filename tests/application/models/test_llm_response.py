import pytest

from src.application.metadata.llm_response_metadata import (
    LLMResponseMetadata,
)
from src.application.models.llm_response import LLMResponse


def build_response(**overrides) -> LLMResponse:
    payload = {
        "text": "Generated answer.",
        "metadata": LLMResponseMetadata(),
    }

    payload.update(overrides)

    return LLMResponse(**payload)


def test_llm_response_can_be_created() -> None:
    response = build_response()

    assert response.text == "Generated answer."
    assert isinstance(response.metadata, LLMResponseMetadata)


def test_llm_response_uses_default_metadata() -> None:
    response = LLMResponse(
        text="Generated answer.",
    )

    assert isinstance(response.metadata, LLMResponseMetadata)


def test_llm_response_is_immutable() -> None:
    response = build_response()

    with pytest.raises(Exception):
        response.text = "Changed"


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_llm_response_rejects_empty_text(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="text cannot be empty",
    ):
        build_response(
            text=value,
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("text", 123),
        ("metadata", {}),
    ],
)
def test_llm_response_rejects_invalid_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_response(
            **{
                field_name: value,
            }
        )