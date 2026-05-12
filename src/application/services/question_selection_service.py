from __future__ import annotations

from src.application.builders.selection_result_builder import (
    SelectionResultBuilder,
)
from src.application.filters.candidate_filter import CandidateFilter
from src.application.policies.selection_policy import SelectionPolicy
from src.application.rankers.candidate_question_ranker import (
    CandidateQuestionRanker,
)
from src.application.validators.question_selection_service_validator import (
    QuestionSelectionServiceValidator,
)
from src.domain.entities.question import Question
from src.domain.results.selection_result import SelectionResult
from src.domain.scoring.scoring_context import ScoringContext


class QuestionSelectionService:
    """
    Question selection orchestration application service.
    """

    def __init__(
        self,
        *,
        candidate_filter: CandidateFilter,
        candidate_ranker: CandidateQuestionRanker,
        selection_policy: SelectionPolicy,
        result_builder: SelectionResultBuilder,
    ) -> None:
        QuestionSelectionServiceValidator.validate_dependencies(
            candidate_filter=candidate_filter,
            candidate_ranker=candidate_ranker,
            selection_policy=selection_policy,
            result_builder=result_builder,
        )

        self._candidate_filter = candidate_filter
        self._candidate_ranker = candidate_ranker
        self._selection_policy = selection_policy
        self._result_builder = result_builder

    def select(
        self,
        *,
        questions: list[Question],
        context: ScoringContext,
    ) -> SelectionResult:
        QuestionSelectionServiceValidator.validate_input(
            questions=questions,
            context=context,
        )

        candidates = self._candidate_filter.filter(
            questions=questions,
            context=context,
        )

        QuestionSelectionServiceValidator.validate_candidates(
            candidates,
        )

        ranked_candidates = self._candidate_ranker.rank(
            questions=candidates,
            context=context,
        )

        QuestionSelectionServiceValidator.validate_ranked_candidates(
            ranked_candidates,
        )

        return self._selection_policy.select(
            ranked_candidates=ranked_candidates,
            context=context,
        )