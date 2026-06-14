from __future__ import annotations

from src.evaluation.rag.calculators.context_recall_score_calculator import ContextRecallScoreCalculator


def test_context_recall_score_should_compare_expected_and_retrieved_context_tokens() -> None:
    assert ContextRecallScoreCalculator().calculate(
        expected_context_tokens={"a", "b"},
        retrieved_context_tokens={"a"},
    ) == 0.5
