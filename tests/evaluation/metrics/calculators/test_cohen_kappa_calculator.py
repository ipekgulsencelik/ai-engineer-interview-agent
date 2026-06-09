from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.cohens_kappa_calculator import (
    CohensKappaCalculator,
)


def test_cohen_kappa_calculator_should_calculate_perfect_agreement() -> None:
    result = CohensKappaCalculator.calculate(
        metric_name="overall_label",
        evaluator_a_labels=(
            "pass",
            "fail",
            "pass",
        ),
        evaluator_b_labels=(
            "pass",
            "fail",
            "pass",
        ),
        p_value=0.01,
        notes="Perfect agreement.",
    )

    assert result.metric_name == "overall_label"
    assert result.kappa_score == pytest.approx(1.0)
    assert result.agreement_ratio == pytest.approx(1.0)
    assert result.sample_count == 3
    assert result.evaluator_count == 2
    assert result.method == "cohen_kappa"
    assert result.is_reliable is True
    assert result.interpretation == "very_strong"
    assert result.p_value == 0.01
    assert result.notes == "Perfect agreement."


def test_cohen_kappa_calculator_should_calculate_partial_agreement() -> None:
    result = CohensKappaCalculator.calculate(
        metric_name="overall_label",
        evaluator_a_labels=(
            "pass",
            "pass",
            "fail",
            "fail",
        ),
        evaluator_b_labels=(
            "pass",
            "fail",
            "fail",
            "pass",
        ),
    )

    assert result.agreement_ratio == pytest.approx(0.5)
    assert -1.0 <= result.kappa_score <= 1.0


def test_cohen_kappa_calculator_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="evaluator label sequences must have the same length",
    ):
        CohensKappaCalculator.calculate(
            metric_name="overall_label",
            evaluator_a_labels=("pass",),
            evaluator_b_labels=("pass", "fail"),
        )


def test_cohen_kappa_calculator_should_raise_for_empty_labels() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="evaluator label sequences cannot be empty",
    ):
        CohensKappaCalculator.calculate(
            metric_name="overall_label",
            evaluator_a_labels=(),
            evaluator_b_labels=(),
        )


def test_cohen_kappa_calculator_should_raise_for_non_string_label() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"evaluator_a_labels\[0\] must be a string",
    ):
        CohensKappaCalculator.calculate(
            metric_name="overall_label",
            evaluator_a_labels=(123, "fail"),  # type: ignore[arg-type]
            evaluator_b_labels=("pass", "fail"),
        )


def test_cohen_kappa_calculator_should_raise_for_empty_string_label() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"evaluator_a_labels\[0\] cannot be empty",
    ):
        CohensKappaCalculator.calculate(
            metric_name="overall_label",
            evaluator_a_labels=("   ", "fail"),
            evaluator_b_labels=("pass", "fail"),
        )


def test_cohen_kappa_calculator_should_raise_for_degenerate_expected_agreement() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="Cohen kappa is undefined",
    ):
        CohensKappaCalculator.calculate(
            metric_name="overall_label",
            evaluator_a_labels=("pass", "pass"),
            evaluator_b_labels=("pass", "pass"),
        )