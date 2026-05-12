import pytest

from src.application.models.evaluation_metadata import (
    EvaluationMetadata,
)
from src.domain.constants.evaluation import (
    DEFAULT_CONFIDENCE_SCORE,
    DEFAULT_RUBRIC_VERSION,
)


def build_metadata(**overrides) -> EvaluationMetadata:
    payload = {
        "confidence": DEFAULT_CONFIDENCE_SCORE,
        "rubric_version": DEFAULT_RUBRIC_VERSION,
        "latency_seconds": None,
        "missing_keywords": (),
        "follow_up_question": None,
    }

    payload.update(overrides)

    return EvaluationMetadata(**payload)


def test_evaluation_metadata_can_be_created() -> None:
    metadata = build_metadata()

    assert metadata.confidence == DEFAULT_CONFIDENCE_SCORE

    assert (
        metadata.rubric_version
        == DEFAULT_RUBRIC_VERSION
    )

    assert metadata.latency_seconds is None

    assert metadata.missing_keywords == ()

    assert metadata.follow_up_question is None


def test_evaluation_metadata_is_immutable() -> None:
    metadata = build_metadata()

    with pytest.raises(Exception):
        metadata.confidence = 1.0


@pytest.mark.parametrize(
    "value",
    [
        -0.1,
        1.1,
    ],
)
def test_evaluation_metadata_rejects_invalid_confidence_range(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            confidence=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_evaluation_metadata_rejects_non_finite_confidence(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            confidence=value,
        )


def test_evaluation_metadata_accepts_nullable_latency() -> None:
    metadata = build_metadata(
        latency_seconds=None,
    )

    assert metadata.latency_seconds is None


def test_evaluation_metadata_rejects_negative_latency() -> None:
    with pytest.raises(ValueError):
        build_metadata(
            latency_seconds=-1.0,
        )


@pytest.mark.parametrize(
    "value",
    [
        ("rag", ""),
        ("rag", " "),
    ],
)
def test_evaluation_metadata_rejects_empty_missing_keywords(
    value: tuple[str, ...],
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            missing_keywords=value,
        )


def test_evaluation_metadata_rejects_invalid_missing_keyword_types() -> None:
    with pytest.raises(TypeError):
        build_metadata(
            missing_keywords=("rag", 123),
        )


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_evaluation_metadata_rejects_empty_follow_up_question(
    value: str,
) -> None:
    with pytest.raises(ValueError):
        build_metadata(
            follow_up_question=value,
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("confidence", True),
        ("rubric_version", 123),
        ("latency_seconds", "fast"),
        ("missing_keywords", ["rag"]),
        ("follow_up_question", 999),
    ],
)
def test_evaluation_metadata_rejects_invalid_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_metadata(
            **{
                field_name: value,
            }
        )