from __future__ import annotations

from src.application.services.adaptive_question_selection_service import (
    AdaptiveQuestionSelectionService,
)
from src.domain.policies.asked_question_history_policy import (
    AskedQuestionHistoryPolicy,
)
from src.domain.policies.interview_score_history_policy import (
    InterviewScoreHistoryPolicy,
)
from src.domain.policies.level_transition_policy import (
    LevelTransitionPolicy,
)
from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.value_objects.interview_state import (
    InterviewState,
)


class InterviewSessionService:
    """
    Adaptive interview session orchestration service.
    """

    def __init__(
        self,
        *,
        question_selection_service: AdaptiveQuestionSelectionService,
        level_transition_policy: LevelTransitionPolicy | None = None,
    ) -> None:
        self._question_selection_service = (
            question_selection_service
        )

        self._level_transition_policy = (
            level_transition_policy
            or LevelTransitionPolicy()
        )

    def select_question(
        self,
        *,
        query: str,
        state: InterviewState,
    ) -> SelectionResult:
        return (
            self._question_selection_service.select_next_question(
                query=query,
                state=state,
            )
        )

    def update_state_after_answer(
        self,
        *,
        state: InterviewState,
        question_id: str,
        evaluation_score: float,
    ) -> InterviewState:
        updated_scores = (
            InterviewScoreHistoryPolicy.append_score(
                recent_scores=state.recent_scores,
                evaluation_score=evaluation_score,
            )
        )

        updated_question_ids = (
            AskedQuestionHistoryPolicy.append_question_id(
                asked_question_ids=(
                    state.asked_question_ids
                ),
                question_id=question_id,
            )
        )

        next_level = (
            self._level_transition_policy.decide(
                current_level=state.current_level,
                recent_scores=list(updated_scores),
            )
        )

        return InterviewState(
            current_level=next_level,
            asked_question_ids=updated_question_ids,
            recent_scores=updated_scores,
            weak_categories=state.weak_categories,
            target_difficulty=state.target_difficulty,
        )