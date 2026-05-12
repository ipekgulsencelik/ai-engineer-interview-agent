from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.domain.metadata.evaluation_metadata import (
    EvaluationMetadata,
)
from src.domain.results.evaluation_result import EvaluationResult


def build_metadata() -> EvaluationMetadata:
    return EvaluationMetadata(
        confidence=0.85,
        rubric_version="v1",
        latency_seconds=None,
        missing_keywords=("RAG",),
        follow_up_question="Explain retrieval quality.",
    )


def build_result() -> EvaluationResult:
    return EvaluationResult(
        score=8.0,
        feedback="Good answer.",
        technical_accuracy=8.0,
        depth=7.0,
        communication=9.0,
        metadata=build_metadata(),
    )


def test_evaluation_result_can_be_created_with_valid_values() -> None:
    result = build_result()

    assert result.score == 8.0
    assert result.feedback == "Good answer."
    assert result.technical_accuracy == 8.0
    assert result.depth == 7.0
    assert result.communication == 9.0
    assert result.metadata.confidence == 0.85


def test_evaluation_result_is_immutable() -> None:
    result = build_result()

    with pytest.raises(FrozenInstanceError):
        result.score = 10.0  # type: ignore[misc]


def test_with_latency_seconds_returns_new_result_instance() -> None:
    result = build_result()

    updated_result = result.with_latency_seconds(
        1.25,
    )

    assert updated_result is not result


def test_with_latency_seconds_preserves_original_result() -> None:
    result = build_result()

    updated_result = result.with_latency_seconds(
        1.25,
    )

    assert result.metadata.latency_seconds is None
    assert updated_result.metadata.latency_seconds == 1.25


def test_with_latency_seconds_preserves_existing_fields() -> None:
    result = build_result()

    updated_result = result.with_latency_seconds(
        0.75,
    )

    assert updated_result.score == result.score
    assert updated_result.feedback == result.feedback
    assert updated_result.technical_accuracy == result.technical_accuracy
    assert updated_result.depth == result.depth
    assert updated_result.communication == result.communication
    assert updated_result.metadata.confidence == result.metadata.confidence
    assert updated_result.metadata.rubric_version == result.metadata.rubric_version
    assert updated_result.metadata.missing_keywords == result.metadata.missing_keywords
    assert updated_result.metadata.follow_up_question == result.metadata.follow_up_question


@pytest.mark.parametrize(
    "score",
    [
        -0.1,
        10.1,
        float("inf"),
        float("nan"),
    ],
)
def test_evaluation_result_rejects_invalid_score(
    score: float,
) -> None:
    with pytest.raises(ValueError):
        EvaluationResult(
            score=score,
            feedback="Valid feedback.",
        )


@pytest.mark.parametrize(
    "feedback",
    [
        "",
        "   ",
    ],
)
def test_evaluation_result_rejects_empty_feedback(
    feedback: str,
) -> None:
    with pytest.raises(ValueError):
        EvaluationResult(
            score=8.0,
            feedback=feedback,
        )


def test_evaluation_result_rejects_boolean_score() -> None:
    with pytest.raises(TypeError):
        EvaluationResult(
            score=True,  # type: ignore[arg-type]
            feedback="Valid feedback.",
        )


def test_evaluation_result_rejects_invalid_metadata() -> None:
    with pytest.raises(TypeError):
        EvaluationResult(
            score=8.0,
            feedback="Valid feedback.",
            metadata=object(),  # type: ignore[arg-type]
        )