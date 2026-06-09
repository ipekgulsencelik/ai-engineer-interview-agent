from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.fleiss_kappa_calculator import (
    FleissKappaCalculator,
)


def test_fleiss_kappa_calculator_should_calculate_perfect_agreement() -> None:
    result = FleissKappaCalculator.calculate(
        metric_name="overall_label",
        label_matrix=(
            (
                "pass",
                "pass",
                "pass",
            ),
            (
                "fail",
                "fail",
                "fail",
            ),
            (
                "pass",
                "pass",
                "pass",
            ),
        ),
        p_value=0.01,
        notes="Perfect agreement.",
    )

    assert result.metric_name == "overall_label"
    assert result.kappa_score == pytest.approx(
        1.0,
    )
    assert result.agreement_ratio == pytest.approx(
        1.0,
    )
    assert result.sample_count == 3
    assert result.evaluator_count == 3
    assert result.method == "fleiss_kappa"
    assert result.is_reliable is True
    assert result.interpretation == "very_strong"
    assert result.p_value == 0.01
    assert result.notes == "Perfect agreement."


def test_fleiss_kappa_calculator_should_calculate_partial_agreement() -> None:
    result = FleissKappaCalculator.calculate(
        metric_name="overall_label",
        label_matrix=(
            (
                "pass",
                "pass",
                "fail",
            ),
            (
                "fail",
                "fail",
                "pass",
            ),
            (
                "pass",
                "pass",
                "pass",
            ),
        ),
    )

    assert result.sample_count == 3
    assert result.evaluator_count == 3
    assert 0.0 <= result.agreement_ratio <= 1.0
    assert -1.0 <= result.kappa_score <= 1.0


def test_fleiss_kappa_calculator_should_raise_for_empty_matrix() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="label_matrix cannot be empty",
    ):
        FleissKappaCalculator.calculate(
            metric_name="overall_label",
            label_matrix=(),
        )


def test_fleiss_kappa_calculator_should_raise_for_single_evaluator() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="Fleiss kappa requires at least 2 evaluators",
    ):
        FleissKappaCalculator.calculate(
            metric_name="overall_label",
            label_matrix=(
                (
                    "pass",
                ),
                (
                    "fail",
                ),
            ),
        )


def test_fleiss_kappa_calculator_should_raise_for_inconsistent_row_lengths() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="all label_matrix rows must have the same evaluator count",
    ):
        FleissKappaCalculator.calculate(
            metric_name="overall_label",
            label_matrix=(
                (
                    "pass",
                    "pass",
                ),
                (
                    "fail",
                    "fail",
                    "fail",
                ),
            ),
        )


def test_fleiss_kappa_calculator_should_raise_for_non_string_label() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"label_matrix\[0\]\[1\] must be a string",
    ):
        FleissKappaCalculator.calculate(
            metric_name="overall_label",
            label_matrix=(
                (
                    "pass",
                    123,  # type: ignore[arg-type]
                ),
                (
                    "fail",
                    "fail",
                ),
            ),
        )


def test_fleiss_kappa_calculator_should_raise_for_empty_label() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"label_matrix\[0\]\[1\] cannot be empty",
    ):
        FleissKappaCalculator.calculate(
            metric_name="overall_label",
            label_matrix=(
                (
                    "pass",
                    "   ",
                ),
                (
                    "fail",
                    "fail",
                ),
            ),
        )