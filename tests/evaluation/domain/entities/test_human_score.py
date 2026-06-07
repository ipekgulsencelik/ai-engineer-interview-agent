from __future__ import annotations

import pytest

from src.evaluation.domain.entities.human_score import (
    HumanScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def test_human_score_should_create_successfully() -> None:
    score = HumanScore(
        sample_id="sample-1",
        evaluator_id="evaluator-1",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        feedback="Strong technical answer with clear explanation.",
    )

    assert score.sample_id == "sample-1"
    assert score.evaluator_id == "evaluator-1"
    assert score.overall_score == 85.0
    assert score.technical_score == 90.0
    assert score.communication_score == 80.0
    assert score.feedback == (
        "Strong technical answer with clear explanation."
    )


def test_human_score_should_raise_for_empty_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_id cannot be empty",
    ):
        HumanScore(
            sample_id="",
            evaluator_id="evaluator-1",
            overall_score=85.0,
            technical_score=90.0,
            communication_score=80.0,
            feedback="Valid feedback.",
        )


def test_human_score_should_raise_for_empty_evaluator_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="evaluator_id cannot be empty",
    ):
        HumanScore(
            sample_id="sample-1",
            evaluator_id="",
            overall_score=85.0,
            technical_score=90.0,
            communication_score=80.0,
            feedback="Valid feedback.",
        )


def test_human_score_should_raise_for_empty_feedback() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="feedback cannot be empty",
    ):
        HumanScore(
            sample_id="sample-1",
            evaluator_id="evaluator-1",
            overall_score=85.0,
            technical_score=90.0,
            communication_score=80.0,
            feedback="",
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_score_should_raise_for_score_below_zero(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "evaluator_id": "evaluator-1",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "feedback": "Valid feedback.",
    }
    kwargs[field_name] = -1.0

    with pytest.raises(
        EvaluationValidationError,
        match=(
            f"{field_name} must be greater than "
            "or equal to 0"
        ),
    ):
        HumanScore(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_score_should_raise_for_score_above_hundred(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "evaluator_id": "evaluator-1",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "feedback": "Valid feedback.",
    }
    kwargs[field_name] = 101.0

    with pytest.raises(
        EvaluationValidationError,
        match=(
            f"{field_name} must be less than "
            "or equal to 100"
        ),
    ):
        HumanScore(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_score_should_raise_for_boolean_score(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "evaluator_id": "evaluator-1",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "feedback": "Valid feedback.",
    }
    kwargs[field_name] = True

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be bool",
    ):
        HumanScore(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_score_should_raise_for_non_finite_score(
    field_name: str,
) -> None:
    kwargs = {
        "sample_id": "sample-1",
        "evaluator_id": "evaluator-1",
        "overall_score": 85.0,
        "technical_score": 90.0,
        "communication_score": 80.0,
        "feedback": "Valid feedback.",
    }
    kwargs[field_name] = float("inf")

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} must be finite",
    ):
        HumanScore(**kwargs)


def test_human_score_should_be_immutable() -> None:
    score = HumanScore(
        sample_id="sample-1",
        evaluator_id="evaluator-1",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        feedback="Valid feedback.",
    )

    with pytest.raises(
        AttributeError,
    ):
        score.sample_id = "changed"  # type: ignore[misc]