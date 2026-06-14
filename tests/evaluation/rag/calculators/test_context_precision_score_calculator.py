from __future__ import annotations

from src.evaluation.rag.calculators.context_precision_score_calculator import ContextPrecisionScoreCalculator


def test_context_precision_score_should_use_context_tokens_as_denominator() -> None:
    assert ContextPrecisionScoreCalculator().calculate(
        answer_tokens={"grounded"},
        context_tokens={"grounded", "extra"},
    ) == 0.5
