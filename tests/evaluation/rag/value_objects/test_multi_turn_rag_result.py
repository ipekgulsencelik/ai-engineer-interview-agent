from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.multi_turn_rag_result import MultiTurnRAGResult
from tests.evaluation.rag.factories import turn_rag_result


def test_multi_turn_rag_result_should_expose_turn_count() -> None:
    result = MultiTurnRAGResult(
        conversation_id="c1",
        turn_results=(turn_rag_result(),),
        average_faithfulness_score=1.0,
        average_answer_relevancy_score=0.5,
        average_context_precision_score=1.0,
        overall_score=0.8,
        interpretation="passed",
    )
    assert result.turn_count == 1


def test_multi_turn_rag_result_should_reject_invalid_overall_score() -> None:
    with pytest.raises(ValueError):
        MultiTurnRAGResult(
            conversation_id="c1",
            turn_results=(),
            average_faithfulness_score=1.0,
            average_answer_relevancy_score=0.5,
            average_context_precision_score=1.0,
            overall_score=2.0,
            interpretation="invalid",
        )
