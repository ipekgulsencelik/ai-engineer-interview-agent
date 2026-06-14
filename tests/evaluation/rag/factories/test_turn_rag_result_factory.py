from __future__ import annotations

from src.evaluation.rag.factories.turn_rag_result_factory import TurnRAGResultFactory


def test_turn_rag_result_factory_should_create_turn_result_with_scores() -> None:
    result = TurnRAGResultFactory.create(
        turn_index=2,
        faithfulness_score=1.0,
        answer_relevancy_score=0.5,
        context_precision_score=0.75,
        overall_score=0.75,
    )

    assert result.turn_index == 2
    assert result.overall_score == 0.75
