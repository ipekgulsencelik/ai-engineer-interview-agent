from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.fleiss_agreement_ratio_calculator import (
    FleissAgreementRatioCalculator,
)


def test_fleiss_agreement_ratio_calculator_should_return_one_for_full_agreement() -> None:
    ratio = FleissAgreementRatioCalculator.calculate(
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
        ),
    )

    assert ratio == pytest.approx(
        1.0,
    )


def test_fleiss_agreement_ratio_calculator_should_calculate_partial_agreement() -> None:
    ratio = FleissAgreementRatioCalculator.calculate(
        label_matrix=(
            (
                "pass",
                "pass",
                "fail",
            ),
            (
                "fail",
                "pass",
                "fail",
            ),
        ),
    )

    assert ratio == pytest.approx(
        1 / 3,
    )