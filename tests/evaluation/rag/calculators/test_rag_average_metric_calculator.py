from __future__ import annotations

import pytest

from src.evaluation.rag.calculators.rag_average_metric_calculator import RAGAverageMetricCalculator


def test_rag_average_metric_should_average_values() -> None:
    assert RAGAverageMetricCalculator.calculate(values=(1.0, 0.5, 0.0)) == pytest.approx(0.5)


def test_rag_average_metric_should_return_zero_for_empty_values() -> None:
    assert RAGAverageMetricCalculator.calculate(values=()) == 0.0
