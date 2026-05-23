from __future__ import annotations

from src.application.services.question_ranking_service import (
    QuestionRankingService,
)
from src.application.services.question_retrieval_service import (
    QuestionRetrievalService,
)
from src.domain.policies.asked_question_filter_policy import (
    AskedQuestionFilterPolicy,
)
from src.domain.policies.question_selection_policy import (
    QuestionSelectionPolicy,
)
from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.value_objects.interview_state import (
    InterviewState,
)


class AdaptiveQuestionSelectionService:
    """
    Adaptive AI interview question selection orchestration.
    """

    def __init__(
        self,
        *,
        retrieval_service: QuestionRetrievalService,
        ranking_service: QuestionRankingService,
        selection_policy: QuestionSelectionPolicy | None = None,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._ranking_service = ranking_service
        self._selection_policy = (
            selection_policy
            or QuestionSelectionPolicy()
        )

    def select_next_question(
        self,
        *,
        query: str,
        state: InterviewState,
        top_k: int = 10,
    ) -> SelectionResult:
        search_results = self._retrieval_service.retrieve(
            query=query,
            context=state,
            top_k=top_k,
        )

        filtered_results = AskedQuestionFilterPolicy.filter(
            search_results=search_results,
            asked_question_ids=state.asked_question_ids,
        )

        ranked_results = self._ranking_service.rank_candidates(
            search_results=filtered_results,
            target_difficulty=state.target_difficulty,
        )

        return self._selection_policy.select_best_candidate(
            ranked_candidates=ranked_results,
        )