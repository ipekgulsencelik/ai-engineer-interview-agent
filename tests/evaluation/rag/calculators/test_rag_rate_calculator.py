from __future__ import annotations

from src.evaluation.rag.calculators.rag_rate_calculator import RAGRateCalculator


def test_rag_rate_should_divide_numerator_by_denominator() -> None:
    assert RAGRateCalculator.calculate(numerator=2, denominator=4) == 0.5


def test_rag_rate_should_return_zero_when_denominator_is_zero() -> None:
    assert RAGRateCalculator.calculate(numerator=2, denominator=0) == 0.0
