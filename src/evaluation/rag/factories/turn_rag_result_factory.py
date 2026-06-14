from __future__ import annotations

from src.evaluation.rag.value_objects.turn_rag_result import (
    TurnRAGResult,
)


class TurnRAGResultFactory:
    """
    Factory for turn-level RAG results.
    """

    @staticmethod
    def create(
        *,
        turn_index: int,
        faithfulness_score: float,
        answer_relevancy_score: float,
        context_precision_score: float,
        overall_score: float,
    ) -> TurnRAGResult:
        return TurnRAGResult(
            turn_index=turn_index,
            faithfulness_score=faithfulness_score,
            answer_relevancy_score=answer_relevancy_score,
            context_precision_score=(
                context_precision_score
            ),
            overall_score=overall_score,
        )