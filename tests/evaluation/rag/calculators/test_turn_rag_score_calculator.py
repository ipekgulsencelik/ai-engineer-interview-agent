from __future__ import annotations

import pytest

from src.evaluation.rag.calculators.turn_rag_score_calculator import TurnRAGScoreCalculator


def test_turn_rag_score_should_average_turn_level_metrics() -> None:
    assert TurnRAGScoreCalculator().calculate(
        faithfulness_score=1.0,
        answer_relevancy_score=0.5,
        context_precision_score=0.0,
    ) == pytest.approx(0.5)
