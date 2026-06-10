from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.overall_alignment_score_calculator import (
    OverallAlignmentScoreCalculator,
)


def test_overall_alignment_score_calculator_should_calculate_score() -> None:
    score = OverallAlignmentScoreCalculator.calculate(
        correlation_score=0.90,
        agreement_score=0.80,
        regression_score=0.70,
    )

    assert score == pytest.approx(0.80)


def test_overall_alignment_score_calculator_should_clamp_negative_regression_score() -> None:
    score = OverallAlignmentScoreCalculator.calculate(
        correlation_score=0.90,
        agreement_score=0.80,
        regression_score=-0.50,
    )

    assert score == pytest.approx(
        (0.90 + 0.80 + 0.0) / 3,
    )


def test_overall_alignment_score_calculator_should_clamp_large_regression_score() -> None:
    score = OverallAlignmentScoreCalculator.calculate(
        correlation_score=0.90,
        agreement_score=0.80,
        regression_score=1.50,
    )

    assert score == pytest.approx(
        (0.90 + 0.80 + 1.0) / 3,
    )