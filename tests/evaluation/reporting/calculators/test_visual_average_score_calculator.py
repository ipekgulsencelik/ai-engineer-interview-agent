from __future__ import annotations

import pytest

from src.evaluation.reporting.calculators.visual_average_score_calculator import VisualAverageScoreCalculator


def test_calculate_returns_average_score() -> None:
    assert VisualAverageScoreCalculator.calculate(scores=(0.5, 0.7, 0.9)) == pytest.approx(0.7)


def test_calculate_returns_none_for_empty_scores() -> None:
    assert VisualAverageScoreCalculator.calculate(scores=()) is None
