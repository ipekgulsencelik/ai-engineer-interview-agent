from __future__ import annotations

from src.evaluation.rag.value_objects.multi_turn_rag_request import (
    MultiTurnRAGRequest,
)
from src.evaluation.rag.services.multi_turn_rag_summary_service import (
    MultiTurnRAGSummaryService,
)
from src.evaluation.rag.services.multi_turn_turn_evaluation_service import (
    MultiTurnTurnEvaluationService,
)
from src.evaluation.rag.value_objects.multi_turn_rag_result import (
    MultiTurnRAGResult,
)


class MultiTurnRAGEvaluator:
    """
    Multi-turn RAG evaluation orchestration service.
    """

    def __init__(
        self,
        *,
        turn_evaluation_service: (
            MultiTurnTurnEvaluationService | None
        ) = None,
        summary_service: MultiTurnRAGSummaryService | None = None,
    ) -> None:
        self._turn_evaluation_service = (
            turn_evaluation_service
            or MultiTurnTurnEvaluationService()
        )
        self._summary_service = (
            summary_service or MultiTurnRAGSummaryService()
        )

    def evaluate(
        self,
        *,
        request: MultiTurnRAGRequest,
    ) -> MultiTurnRAGResult:
        turn_results = self._turn_evaluation_service.evaluate_turns(
            turns=request.turns,
        )

        return self._summary_service.summarize(
            request=request,
            turn_results=turn_results,
        )