from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.benchmark_score_calculator import (
    BenchmarkScoreCalculator,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
    _category_snapshot,
)


def test_benchmark_score_calculator_should_use_alignment_score_when_no_categories() -> None:
    score = BenchmarkScoreCalculator.calculate(
        alignment_report=_alignment_report(),
        category_snapshots=(),
    )

    assert score == pytest.approx(0.80)


def test_benchmark_score_calculator_should_calculate_weighted_score() -> None:
    score = BenchmarkScoreCalculator.calculate(
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(
                category="RAG",
                score=0.90,
            ),
            _category_snapshot(
                category="Agents",
                score=0.70,
            ),
        ),
    )

    assert score == pytest.approx(0.80)