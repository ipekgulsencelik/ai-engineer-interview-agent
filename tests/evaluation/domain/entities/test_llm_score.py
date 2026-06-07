from __future__ import annotations

import pytest

from src.evaluation.domain.entities.llm_score import (
    LLMScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def test_llm_score_should_create_successfully() -> None:
    score = LLMScore(
        sample_id="sample-1",
        model_name="gpt-5",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        reasoning_score=88.0,
        confidence_score=92.0,
        feedback="Strong answer.",
    )

    assert score.sample_id == "sample-1"
    assert score.model_name == "gpt-5"
    assert score.overall_score == 85.0
    assert score.technical_score == 90.0
    assert score.communication_score == 80.0
    assert score.reasoning_score == 88.0
    assert score.confidence_score == 92.0
    assert score.feedback == "Strong answer."


def test_llm_score_should_raise_for_empty_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_id cannot be empty",
    ):
        LLMScore(
            sample_id="",
            model_name="gpt-5",
            overall_score=85.0,
            technical_score=90.0,
            communication_score=80.0,
            reasoning_score=88.0,
            confidence_score=92.0,
            feedback="Strong answer.",
        )


def test_llm_score_should_raise_for_empty_model_name() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="model_name cannot be empty",
    ):
        LLMScore(
            sample_id="sample-1",
            model_name="",
            overall_score=85.0,
            technical_score=90.0,
            communication_score=80.0,
            reasoning_score=88.0,
            confidence_score=92.0,
            feedback="Strong answer.",
        )


def test_llm_score_should_raise_for_empty_feedback() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="feedback cannot be empty",
    ):
        LLMScore(
            sample_id="sample-1",
            model_name="gpt-5",
            overall_score=85.0,
            technical_score=90.0,
            communication_score=80.0,
            reasoning_score=88.0,
            confidence_score=92.0,
            feedback="",
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
        "reasoning_score",
        "confidence_score",
    ],
)
def test_llm_score_should_raise_for_score_below_zero(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "model_name": "gpt-5",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "reasoning_score": 88.0,
        "confidence_score": 92.0,
        "feedback": "Strong answer.",
    }

    kwargs[field_name] = -1.0

    with pytest.raises(
        EvaluationValidationError,
        match=(
            f"{field_name} must be greater than "
            "or equal to 0"
        ),
    ):
        LLMScore(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
        "reasoning_score",
        "confidence_score",
    ],
)
def test_llm_score_should_raise_for_score_above_hundred(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "model_name": "gpt-5",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "reasoning_score": 88.0,
        "confidence_score": 92.0,
        "feedback": "Strong answer.",
    }

    kwargs[field_name] = 101.0

    with pytest.raises(
        EvaluationValidationError,
        match=(
            f"{field_name} must be less than "
            "or equal to 100"
        ),
    ):
        LLMScore(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
        "reasoning_score",
        "confidence_score",
    ],
)
def test_llm_score_should_raise_for_boolean_score(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "model_name": "gpt-5",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "reasoning_score": 88.0,
        "confidence_score": 92.0,
        "feedback": "Strong answer.",
    }

    kwargs[field_name] = True

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be bool",
    ):
        LLMScore(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
        "reasoning_score",
        "confidence_score",
    ],
)
def test_llm_score_should_raise_for_non_finite_score(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "model_name": "gpt-5",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "reasoning_score": 88.0,
        "confidence_score": 92.0,
        "feedback": "Strong answer.",
    }

    kwargs[field_name] = float("inf")

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} must be finite",
    ):
        LLMScore(**kwargs)


def test_llm_score_should_be_immutable() -> None:
    score = LLMScore(
        sample_id="sample-1",
        model_name="gpt-5",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        reasoning_score=88.0,
        confidence_score=92.0,
        feedback="Strong answer.",
    )

    with pytest.raises(
        AttributeError,
    ):
        score.sample_id = "changed"  # type: ignore[misc]