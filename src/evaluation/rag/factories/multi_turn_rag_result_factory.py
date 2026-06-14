from __future__ import annotations

from src.evaluation.rag.value_objects.multi_turn_rag_result import (
    MultiTurnRAGResult,
)
from src.evaluation.rag.value_objects.turn_rag_result import (
    TurnRAGResult,
)


class MultiTurnRAGResultFactory:
    """
    Factory for multi-turn RAG results.
    """

    @staticmethod
    def create(
        *,
        conversation_id: str,
        turn_results: tuple[
            TurnRAGResult,
            ...,
        ],
        average_faithfulness_score: float,
        average_answer_relevancy_score: float,
        average_context_precision_score: float,
        overall_score: float,
        interpretation: str,
        notes: str | None = None,
    ) -> MultiTurnRAGResult:
        return MultiTurnRAGResult(
            conversation_id=conversation_id,
            turn_results=turn_results,
            average_faithfulness_score=(
                average_faithfulness_score
            ),
            average_answer_relevancy_score=(
                average_answer_relevancy_score
            ),
            average_context_precision_score=(
                average_context_precision_score
            ),
            overall_score=overall_score,
            interpretation=interpretation,
            notes=notes,
        )