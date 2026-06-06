from __future__ import annotations

from dataclasses import dataclass

from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.application.services.level_transition_service import (
    LevelTransitionService,
)
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)
from src.application.services.question_selection_service import (
    QuestionSelectionService,
)
from src.domain.scoring.scoring_context import ScoringContext


@dataclass(frozen=True)
class RunInterviewStepPayload:
    query: str
    answer: str
    context: ScoringContext
    top_k: int = 5


@dataclass(frozen=True)
class InterviewStepResult:
    selection_result: object
    evaluation_result: object
    next_level: object


class RunInterviewStepUseCase:
    """
    Adaptive interview step orchestration use case.
    """

    def __init__(
        self,
        *,
        question_retrieval_service: QuestionRetrievalService,
        question_selection_service: QuestionSelectionService,
        answer_evaluation_service: AnswerEvaluationService,
        level_transition_service: LevelTransitionService,
    ) -> None:
        self._question_retrieval_service = question_retrieval_service
        self._question_selection_service = question_selection_service
        self._answer_evaluation_service = answer_evaluation_service
        self._level_transition_service = level_transition_service

    def execute(
        self,
        *,
        payload: RunInterviewStepPayload,
    ) -> InterviewStepResult:
        questions = self._question_retrieval_service.retrieve(
            query=payload.query,
            context=payload.context,
            top_k=payload.top_k,
        )

        selection_result = self._question_selection_service.select(
            questions=questions,
            context=payload.context,
        )

        evaluation_result = self._answer_evaluation_service.evaluate(
            question=selection_result.question,
            answer=payload.answer,
        )

        next_level = self._level_transition_service.transition(
            current_level=payload.context.current_level,
            recent_scores=[
                *payload.context.recent_scores,
                evaluation_result.score,
            ],
        )

        return InterviewStepResult(
            selection_result=selection_result,
            evaluation_result=evaluation_result,
            next_level=next_level,
        )