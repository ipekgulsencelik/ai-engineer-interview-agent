from __future__ import annotations

import pytest

from src.evaluation.domain.entities.alignment_result import (
    AlignmentResult,
)
from src.evaluation.domain.enums.agreement_level import (
    AgreementLevel,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _valid_alignment_result_kwargs() -> dict:
    return {
        "sample_id": "sample-1",
        "alignment_evaluation_id": "alignment-1",
        "alignment_evaluation_timestamp": "2026-06-06T20:00:00+03:00",
        "alignment_evaluation_version": "1.0.0",
        "alignment_evaluation_criteria": "Compare human and LLM scores.",
        "alignment_evaluation_feedback": "Strong agreement.",
        "pearson_correlation": 0.92,
        "cohen_kappa": 0.84,
        "mean_absolute_error": 4.5,
        "agreement_level": AgreementLevel.HIGH,
        "llm_model_name": "gpt-5",
        "human_evaluator_id": "evaluator-1",
        "overall_alignment_score": 88.0,
        "technical_alignment_score": 90.0,
        "communication_alignment_score": 85.0,
        "reasoning_alignment_score": 87.0,
    }


def test_alignment_result_should_create_successfully() -> None:
    result = AlignmentResult(
        **_valid_alignment_result_kwargs(),
    )

    assert result.sample_id == "sample-1"
    assert result.alignment_evaluation_id == "alignment-1"
    assert result.alignment_evaluation_version == "1.0.0"
    assert result.pearson_correlation == 0.92
    assert result.cohen_kappa == 0.84
    assert result.mean_absolute_error == 4.5
    assert result.agreement_level is AgreementLevel.HIGH
    assert result.llm_model_name == "gpt-5"
    assert result.human_evaluator_id == "evaluator-1"
    assert result.overall_alignment_score == 88.0


@pytest.mark.parametrize(
    "field_name",
    [
        "sample_id",
        "alignment_evaluation_id",
        "alignment_evaluation_timestamp",
        "alignment_evaluation_version",
        "alignment_evaluation_criteria",
        "alignment_evaluation_feedback",
        "llm_model_name",
        "human_evaluator_id",
    ],
)
def test_alignment_result_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be empty",
    ):
        AlignmentResult(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "pearson_correlation",
        "cohen_kappa",
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        -1.1,
        1.1,
    ],
)
def test_alignment_result_should_raise_for_invalid_correlation_fields(
    field_name: str,
    invalid_value: float,
) -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs[field_name] = invalid_value

    with pytest.raises(
        EvaluationValidationError,
        match=field_name,
    ):
        AlignmentResult(**kwargs)


def test_alignment_result_should_raise_for_negative_mean_absolute_error() -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs["mean_absolute_error"] = -0.1

    with pytest.raises(
        EvaluationValidationError,
        match=(
            "mean_absolute_error must be greater than "
            "or equal to 0"
        ),
    ):
        AlignmentResult(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_alignment_score",
        "technical_alignment_score",
        "communication_alignment_score",
        "reasoning_alignment_score",
    ],
)
def test_alignment_result_should_raise_for_score_below_zero(
    field_name: str,
) -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs[field_name] = -1.0

    with pytest.raises(
        EvaluationValidationError,
        match=(
            f"{field_name} must be greater than "
            "or equal to 0"
        ),
    ):
        AlignmentResult(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_alignment_score",
        "technical_alignment_score",
        "communication_alignment_score",
        "reasoning_alignment_score",
    ],
)
def test_alignment_result_should_raise_for_score_above_hundred(
    field_name: str,
) -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs[field_name] = 101.0

    with pytest.raises(
        EvaluationValidationError,
        match=(
            f"{field_name} must be less than "
            "or equal to 100"
        ),
    ):
        AlignmentResult(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "pearson_correlation",
        "cohen_kappa",
        "mean_absolute_error",
        "overall_alignment_score",
        "technical_alignment_score",
        "communication_alignment_score",
        "reasoning_alignment_score",
    ],
)
def test_alignment_result_should_raise_for_boolean_numeric_fields(
    field_name: str,
) -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs[field_name] = True

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be bool",
    ):
        AlignmentResult(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "pearson_correlation",
        "cohen_kappa",
        "mean_absolute_error",
        "overall_alignment_score",
        "technical_alignment_score",
        "communication_alignment_score",
        "reasoning_alignment_score",
    ],
)
def test_alignment_result_should_raise_for_non_finite_numeric_fields(
    field_name: str,
) -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs[field_name] = float("inf")

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} must be finite",
    ):
        AlignmentResult(**kwargs)


def test_alignment_result_should_raise_for_invalid_agreement_level() -> None:
    kwargs = _valid_alignment_result_kwargs()
    kwargs["agreement_level"] = "HIGH"

    with pytest.raises(
        EvaluationValidationError,
        match="agreement_level must be an AgreementLevel enum",
    ):
        AlignmentResult(**kwargs)


def test_alignment_result_should_be_immutable() -> None:
    result = AlignmentResult(
        **_valid_alignment_result_kwargs(),
    )

    with pytest.raises(
        AttributeError,
    ):
        result.sample_id = "changed"  # type: ignore[misc]