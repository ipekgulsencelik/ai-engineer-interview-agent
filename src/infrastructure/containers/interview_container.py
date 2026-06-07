from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from src.application.services.level_transition_service import LevelTransitionService
from src.application.services.question_selection_service import (
    QuestionSelectionService,
    HighestScoreSelectionPolicy,
)
from src.application.use_cases.run_interview_step_use_case import RunInterviewStepUseCase
from src.infrastructure.containers.base_container import BaseContainer

if TYPE_CHECKING:
    from src.infrastructure.containers.evaluation_container import EvaluationContainer
    from src.infrastructure.containers.retrieval_container import RetrievalContainer
    from src.infrastructure.containers.scoring_container import ScoringContainer


class InterviewContainer(BaseContainer):
    """
    Interview dependency container.
    """

    def __init__(
        self,
        *,
        retrieval_container: RetrievalContainer,
        scoring_container: ScoringContainer,
        evaluation_container: EvaluationContainer,
    ) -> None:
        self._retrieval_container = retrieval_container

        self._scoring_container = scoring_container

        self._evaluation_container = (
            evaluation_container
        )

    @cached_property
    def question_selection_service(
        self,
    ) -> QuestionSelectionService:
        return QuestionSelectionService(
            scoring_engine=(
                self._scoring_container.scoring_engine
            ),
            selection_policy=(
                HighestScoreSelectionPolicy()
            ),
        )

    @cached_property
    def level_transition_service(
        self,
    ) -> LevelTransitionService:
        return LevelTransitionService()

    @cached_property
    def run_interview_step_use_case(
        self,
    ) -> RunInterviewStepUseCase:
        return RunInterviewStepUseCase(
            question_retrieval_service=(
                self._retrieval_container
                .question_retrieval_service
            ),
            question_selection_service=(
                self.question_selection_service
            ),
            answer_evaluation_service=(
                self._evaluation_container
                .answer_evaluation_service
            ),
            level_transition_service=(
                self.level_transition_service
            ),
        )