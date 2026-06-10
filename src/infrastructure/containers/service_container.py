from __future__ import annotations

from collections.abc import Callable
from functools import cached_property
from typing import TYPE_CHECKING

from src.application.ports.llm_client import LLMClient
from src.config.settings import settings
from src.infrastructure.llm.groq_llm_client import GroqLLMClient


if TYPE_CHECKING:
    from src.application.services.adaptive_question_selection_service import (
        AdaptiveQuestionSelectionService,
    )
    from src.application.services.answer_evaluation_service import (
        AnswerEvaluationService,
    )
    from src.application.services.cv_analysis_orchestration_service import (
        CVAnalysisOrchestrationService,
    )
    from src.application.services.semantic_question_retrieval_service import (
        SemanticQuestionRetrievalService,
    )
    from src.application.use_cases.run_interview_step_use_case import (
        RunInterviewStepUseCase,
    )
    from src.infrastructure.containers.cv_container import CVContainer
    from src.infrastructure.containers.evaluation_container import EvaluationContainer
    from src.infrastructure.containers.interview_container import InterviewContainer
    from src.infrastructure.containers.retrieval_container import RetrievalContainer
    from src.infrastructure.containers.scoring_container import ScoringContainer


class ServiceContainer:
    """
    Application composition root facade.

    Container sub-components are lazily imported so FastAPI startup only loads
    the dependency graph that is actually needed.
    """

    def __init__(
        self,
        *,
        llm_client_factory: Callable[[], LLMClient] | None = None,
    ) -> None:
        self._llm_client_factory = llm_client_factory or self._build_groq_client

    @staticmethod
    def _build_groq_client() -> LLMClient:
        return GroqLLMClient(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_NAME,
        )

    @cached_property
    def retrieval(self) -> RetrievalContainer:
        from src.infrastructure.containers.retrieval_container import RetrievalContainer

        return RetrievalContainer()

    @cached_property
    def scoring(self) -> ScoringContainer:
        from src.infrastructure.containers.scoring_container import ScoringContainer

        return ScoringContainer()

    @cached_property
    def evaluation(self) -> EvaluationContainer:
        from src.infrastructure.containers.evaluation_container import EvaluationContainer

        return EvaluationContainer()

    @cached_property
    def llm_client(self) -> LLMClient:
        return self._llm_client_factory()

    @cached_property
    def interview(self) -> InterviewContainer:
        from src.infrastructure.containers.interview_container import InterviewContainer

        return InterviewContainer(
            retrieval_container=None,
            scoring_container=None,
            evaluation_container=self.evaluation,
        )

    @cached_property
    def cv(self) -> CVContainer:
        from src.infrastructure.containers.cv_container import CVContainer

        return CVContainer(
            llm_client=self.llm_client,
        )

    @property
    def answer_evaluation_service(self) -> AnswerEvaluationService:
        return self.evaluation.answer_evaluation_service

    @property
    def run_interview_step_use_case(self) -> RunInterviewStepUseCase:
        return self.interview.run_interview_step_use_case

    @property
    def adaptive_selection_service(self) -> AdaptiveQuestionSelectionService:
        return self.retrieval.adaptive_selection_service

    @property
    def question_retrieval_service(self) -> SemanticQuestionRetrievalService:
        return self.retrieval.question_retrieval_service

    @property
    def cv_analysis_orchestration_service(self) -> CVAnalysisOrchestrationService:
        return self.cv.cv_analysis_orchestration_service
