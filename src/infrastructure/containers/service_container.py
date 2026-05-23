from __future__ import annotations

from functools import cached_property

from src.application.ports.llm_client import (
    LLMClient,
)
from src.infrastructure.clients.groq_llm_client import (
    GroqLLMClient,
)
from src.infrastructure.containers.cv_container import (
    CVContainer,
)
from src.infrastructure.containers.evaluation_container import (
    EvaluationContainer,
)
from src.infrastructure.containers.interview_container import (
    InterviewContainer,
)
from src.infrastructure.containers.retrieval_container import (
    RetrievalContainer,
)
from src.infrastructure.containers.scoring_container import (
    ScoringContainer,
)


class ServiceContainer:
    """
    Application composition root facade.
    """

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
        return GroqLLMClient()

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
        return (
            self.evaluation
            .answer_evaluation_service
        )

    @property
    def run_interview_step_use_case(
        self,
    ):
        return (
            self.interview
            .run_interview_step_use_case
        )

    @property
    def question_retrieval_service(
        self,
    ):
        return (
            self.retrieval
            .question_retrieval_service
        )

    @property
    def cv_analysis_orchestration_service(
        self,
    ):
        return (
            self.cv
            .cv_analysis_orchestration_service
        )