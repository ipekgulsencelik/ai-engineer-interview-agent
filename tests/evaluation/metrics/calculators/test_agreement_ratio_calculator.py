from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.agreement_ratio_calculator import (
    AgreementRatioCalculator,
)


def test_agreement_ratio_calculator_should_return_one_for_full_agreement() -> None:
    ratio = AgreementRatioCalculator.calculate(
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
    )

    assert ratio == pytest.approx(1.0)


def test_agreement_ratio_calculator_should_calculate_partial_agreement() -> None:
    ratio = AgreementRatioCalculator.calculate(
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

    assert ratio == pytest.approx(0.5)


def test_agreement_ratio_calculator_should_return_zero_for_no_agreement() -> None:
    ratio = AgreementRatioCalculator.calculate(
        evaluator_a_labels=(
            "pass",
            "pass",
        ),
        evaluator_b_labels=(
            "fail",
            "fail",
        ),
    )

    assert ratio == pytest.approx(0.0)