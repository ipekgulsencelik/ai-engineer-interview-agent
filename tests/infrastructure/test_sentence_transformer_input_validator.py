import pytest

from src.infrastructure.validators.sentence_transformer_input_validator import (
    SentenceTransformerInputValidator,
)


def test_validate_text_strips_whitespace() -> None:
    assert SentenceTransformerInputValidator.validate_text("  hello  ") == "hello"


def test_validate_text_raises_for_non_string() -> None:
    with pytest.raises(TypeError, match="Text must be a string"):
        SentenceTransformerInputValidator.validate_text(123)  # type: ignore[arg-type]


def test_validate_text_raises_for_empty() -> None:
    with pytest.raises(ValueError, match="Text cannot be empty"):
        SentenceTransformerInputValidator.validate_text("   ")


def test_validate_texts_raises_for_empty_list() -> None:
    with pytest.raises(ValueError, match="Texts cannot be empty"):
        SentenceTransformerInputValidator.validate_texts([])


def test_validate_texts_normalizes_all_items() -> None:
    assert SentenceTransformerInputValidator.validate_texts([" a ", "b "]) == ["a", "b"]
