from __future__ import annotations

from src.evaluation.rag.services.multi_turn_turn_evaluation_service import MultiTurnTurnEvaluationService
from tests.evaluation.rag.factories import conversation_turn


def test_multi_turn_turn_evaluation_service_should_evaluate_one_turn() -> None:
    result = MultiTurnTurnEvaluationService().evaluate_turn(
        turn=conversation_turn(user_message="rag context", assistant_message="rag context", retrieved_context="rag context")
    )

    assert result.turn_index == 0
    assert result.faithfulness_score == 1.0
    assert result.context_precision_score == 1.0


def test_multi_turn_turn_evaluation_service_should_return_zero_context_scores_without_retrieved_context() -> None:
    result = MultiTurnTurnEvaluationService().evaluate_turn(
        turn=conversation_turn(retrieved_context=None)
    )

    assert result.faithfulness_score == 0.0
    assert result.context_precision_score == 0.0
