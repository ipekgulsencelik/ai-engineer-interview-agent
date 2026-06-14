from __future__ import annotations

from src.evaluation.rag.constants.rag_thresholds import (
    MINIMUM_OVERALL_RAG_SCORE,
)


class MultiTurnRAGInterpreter:
    """
    Produces interpretation label for multi-turn RAG results.
    """

    @staticmethod
    def interpret(
        *,
        overall_score: float,
    ) -> str:
        if overall_score >= MINIMUM_OVERALL_RAG_SCORE:
            return "multi_turn_rag_passed"

        return "multi_turn_rag_failed"