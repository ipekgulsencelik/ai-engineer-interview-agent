from __future__ import annotations

from src.evaluation.rag.evaluators.multi_turn_rag_evaluator import MultiTurnRAGEvaluator
from src.evaluation.rag.value_objects.multi_turn_rag_request import MultiTurnRAGRequest
from tests.evaluation.rag.factories import conversation_turn


def test_multi_turn_rag_evaluator_should_evaluate_turns_and_summarize_conversation() -> None:
    result = MultiTurnRAGEvaluator().evaluate(
        request=MultiTurnRAGRequest(
            conversation_id="conversation-1",
            turns=(conversation_turn(user_message="rag context", assistant_message="rag context", retrieved_context="rag context"),),
        )
    )

    assert result.conversation_id == "conversation-1"
    assert result.turn_count == 1
    assert result.overall_score > 0.0
