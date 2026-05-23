from __future__ import annotations

from collections.abc import Callable
from functools import cached_property

from src.application.ports.llm_client import LLMClient
from src.infrastructure.containers.cv_container import CVContainer
from src.infrastructure.containers.evaluation_container import (
    EvaluationContainer,
)
from src.infrastructure.containers.interview_container import (
    InterviewContainer,
)
from src.infrastructure.containers.retrieval_container import (
    RetrievalContainer,
)
from src.infrastructure.containers.scoring_container import ScoringContainer
from src.infrastructure.llm.groq_llm_client import GroqLLMClient


class ServiceContainer:
    """
    Application composition root facade.
    """

    def __init__(
        self,
        *,
        llm_client_factory: Callable[[], LLMClient] | None = None,
    ) -> None:
        self._llm_client_factory = (
            llm_client_factory
            or GroqLLMClient
        )

    @cached_property
    def retrieval(
        self,
    ) -> RetrievalContainer:
        return RetrievalContainer()

    @cached_property
    def scoring(
        self,
    ) -> ScoringContainer:
        return ScoringContainer()

    @cached_property
    def evaluation(
        self,
    ) -> EvaluationContainer:
        return EvaluationContainer()

    @cached_property
    def llm_client(
        self,
    ) -> LLMClient:
        return self._llm_client_factory()

    @cached_property
    def interview(
        self,
    ) -> InterviewContainer:
        return InterviewContainer(
            retrieval_container=self.retrieval,
            scoring_container=self.scoring,
            evaluation_container=self.evaluation,
        )

    @cached_property
    def cv(
        self,
    ) -> CVContainer:
        return CVContainer(
            llm_client=self.llm_client,
        )

    @property
    def answer_evaluation_service(
        self,
    ):
        return self.evaluation.answer_evaluation_service

    @property
    def run_interview_step_use_case(
        self,
    ):
        return self.interview.run_interview_step_use_case

    @property
    def question_retrieval_service(
        self,
    ):
        return self.retrieval.question_retrieval_service

    @property
    def cv_analysis_orchestration_service(
        self,
    ):
        return self.cv.cv_analysis_orchestration_service
