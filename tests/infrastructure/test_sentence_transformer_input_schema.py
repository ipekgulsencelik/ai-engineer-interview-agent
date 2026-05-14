import pytest

from src.infrastructure.validations.sentence_transformer_input_schema import (
    SentenceTransformerBatchTextSchema,
    SentenceTransformerTextSchema,
)


def test_text_schema_parse_normalizes_text() -> None:
    parsed = SentenceTransformerTextSchema.parse("  hello  ")
    assert parsed.text == "hello"


def test_text_schema_parse_raises_for_non_string() -> None:
    with pytest.raises(TypeError, match="Text must be a string"):
        SentenceTransformerTextSchema.parse(123)  # type: ignore[arg-type]


def test_batch_schema_parse_normalizes_items() -> None:
    parsed = SentenceTransformerBatchTextSchema.parse([" a ", "b "])
    assert parsed.texts == ["a", "b"]


def test_batch_schema_parse_raises_for_non_list() -> None:
    with pytest.raises(TypeError, match="Texts must be a list of strings"):
        SentenceTransformerBatchTextSchema.parse("x")  # type: ignore[arg-type]