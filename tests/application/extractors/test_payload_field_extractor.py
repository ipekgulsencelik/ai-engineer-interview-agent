import pytest

from src.application.extractors.payload_field_extractor import (
    PayloadFieldExtractor,
)


def test_get_required_string_returns_trimmed_string() -> None:
    payload = {
        "feedback": "  Good answer.  ",
    }

    result = PayloadFieldExtractor.get_required_string(
        payload,
        "feedback",
    )

    assert result == "Good answer."


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_get_required_string_rejects_empty_string(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="feedback cannot be empty",
    ):
        PayloadFieldExtractor.get_required_string(
            {"feedback": value},
            "feedback",
        )


def test_get_required_string_rejects_invalid_type() -> None:
    with pytest.raises(
        TypeError,
        match="feedback must be a string",
    ):
        PayloadFieldExtractor.get_required_string(
            {"feedback": 123},
            "feedback",
        )


def test_get_optional_string_returns_none_when_missing() -> None:
    result = PayloadFieldExtractor.get_optional_string(
        {},
        "follow_up_question",
    )

    assert result is None


def test_get_optional_string_returns_trimmed_string() -> None:
    result = PayloadFieldExtractor.get_optional_string(
        {
            "follow_up_question": "  Explain vector DB.  ",
        },
        "follow_up_question",
    )

    assert result == "Explain vector DB."


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_get_optional_string_rejects_empty_string(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="follow_up_question cannot be empty",
    ):
        PayloadFieldExtractor.get_optional_string(
            {"follow_up_question": value},
            "follow_up_question",
        )


@pytest.mark.parametrize(
    "value",
    [
        8,
        8.5,
    ],
)
def test_get_required_float_returns_float(
    value,
) -> None:
    result = PayloadFieldExtractor.get_required_float(
        {
            "score": value,
        },
        "score",
    )

    assert result == float(value)


@pytest.mark.parametrize(
    "value",
    [
        True,
        "8.5",
        None,
        [],
    ],
)
def test_get_required_float_rejects_invalid_types(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="score must be numeric",
    ):
        PayloadFieldExtractor.get_required_float(
            {
                "score": value,
            },
            "score",
        )


@pytest.mark.parametrize(
    "value",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_get_required_float_rejects_non_finite_values(
    value: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="score must be finite",
    ):
        PayloadFieldExtractor.get_required_float(
            {
                "score": value,
            },
            "score",
        )


def test_get_optional_float_returns_default_when_missing() -> None:
    result = PayloadFieldExtractor.get_optional_float(
        {},
        "confidence",
        default=0.0,
    )

    assert result == 0.0


def test_get_optional_float_returns_float_when_present() -> None:
    result = PayloadFieldExtractor.get_optional_float(
        {
            "confidence": 0.85,
        },
        "confidence",
        default=0.0,
    )

    assert result == 0.85


def test_get_optional_string_tuple_returns_empty_tuple_when_missing() -> None:
    result = PayloadFieldExtractor.get_optional_string_tuple(
        {},
        "missing_keywords",
    )

    assert result == ()


def test_get_optional_string_tuple_normalizes_list_to_tuple() -> None:
    result = PayloadFieldExtractor.get_optional_string_tuple(
        {
            "missing_keywords": [
                " rag ",
                " vector db ",
            ],
        },
        "missing_keywords",
    )

    assert result == (
        "rag",
        "vector db",
    )


def test_get_optional_string_tuple_rejects_non_list_value() -> None:
    with pytest.raises(
        TypeError,
        match="missing_keywords must be a list",
    ):
        PayloadFieldExtractor.get_optional_string_tuple(
            {
                "missing_keywords": "rag",
            },
            "missing_keywords",
        )


def test_get_optional_string_tuple_rejects_invalid_item_type() -> None:
    with pytest.raises(
        TypeError,
        match="All items in missing_keywords must be strings",
    ):
        PayloadFieldExtractor.get_optional_string_tuple(
            {
                "missing_keywords": [
                    "rag",
                    123,
                ],
            },
            "missing_keywords",
        )


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_get_optional_string_tuple_rejects_empty_items(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Items in missing_keywords cannot be empty",
    ):
        PayloadFieldExtractor.get_optional_string_tuple(
            {
                "missing_keywords": [
                    "rag",
                    value,
                ],
            },
            "missing_keywords",
        )