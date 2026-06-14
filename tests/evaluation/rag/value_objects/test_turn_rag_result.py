from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.turn_rag_result import TurnRAGResult


def test_turn_rag_result_should_store_turn_scores() -> None:
    result = TurnRAGResult(turn_index=1, faithfulness_score=1.0, answer_relevancy_score=0.5, context_precision_score=0.5, overall_score=0.67)
    assert result.turn_index == 1
    assert result.overall_score == 0.67


def test_turn_rag_result_should_reject_negative_turn_index() -> None:
    with pytest.raises(ValueError):
        TurnRAGResult(turn_index=-1, faithfulness_score=1.0, answer_relevancy_score=0.5, context_precision_score=0.5, overall_score=0.67)
