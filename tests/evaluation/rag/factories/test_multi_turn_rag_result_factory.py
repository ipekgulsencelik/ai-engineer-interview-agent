from __future__ import annotations

from src.evaluation.rag.factories.multi_turn_rag_result_factory import MultiTurnRAGResultFactory
from tests.evaluation.rag.factories import turn_rag_result


def test_multi_turn_rag_result_factory_should_create_result_with_turns_and_averages() -> None:
    result = MultiTurnRAGResultFactory.create(
        conversation_id="conversation-1",
        turn_results=(turn_rag_result(),),
        average_faithfulness_score=1.0,
        average_answer_relevancy_score=0.5,
        average_context_precision_score=1.0,
        overall_score=0.8,
        interpretation="passed",
    )

    assert result.conversation_id == "conversation-1"
    assert result.turn_count == 1
