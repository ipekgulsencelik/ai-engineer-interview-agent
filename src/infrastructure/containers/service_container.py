from __future__ import annotations

from collections.abc import Callable
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING

from src.application.ports.llm_client import LLMClient
from src.config.settings import settings
from src.infrastructure.config.app_paths import DEFAULT_QUESTION_BANK_PATH

if TYPE_CHECKING:
    from src.application.ports.embedding_provider import EmbeddingProvider
    from src.application.services.adaptive_question_selection_service import (
        AdaptiveQuestionSelectionService,
    )
    from src.application.services.answer_evaluation_service import (
        AnswerEvaluationService,
    )
    from src.application.services.cv_analysis_orchestration_service import (
        CVAnalysisOrchestrationService,
    )
    from src.application.services.interview_session_service import (
        InterviewSessionService,
    )
    from src.application.services.semantic_question_retrieval_service import (
        SemanticQuestionRetrievalService,
    )
    from src.infrastructure.containers.cv_container import CVContainer
    from src.infrastructure.containers.evaluation_container import EvaluationContainer
    from src.infrastructure.containers.retrieval_container import RetrievalContainer


def _groq_client_factory() -> LLMClient:
    from src.infrastructure.llm.groq_llm_client import GroqLLMClient

    return GroqLLMClient(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL_NAME,
    )


class ServiceContainer:
    """
    Application composition root facade.

    Sub-containers are imported lazily so startup only loads what a request
    needs. Every external dependency can be overridden for tests:

    - llm_client_factory: None -> Groq when GROQ_API_KEY is set, otherwise no
      LLM (offline keyword evaluator, CV analysis unavailable)
    - embedding_provider / chroma_persist_directory: semantic retrieval
    - use_semantic_retrieval: False skips the embedding model entirely
    """

    def __init__(
        self,
        *,
        llm_client_factory: Callable[[], LLMClient] | None = None,
        question_bank_path: Path | str = DEFAULT_QUESTION_BANK_PATH,
        embedding_provider: EmbeddingProvider | None = None,
        chroma_persist_directory: str | None = None,
        use_semantic_retrieval: bool = True,
    ) -> None:
        if llm_client_factory is None and settings.GROQ_API_KEY.strip():
            llm_client_factory = _groq_client_factory
        self._llm_client_factory = llm_client_factory
        self._question_bank_path = Path(question_bank_path)
        self._embedding_provider = embedding_provider
        self._chroma_persist_directory = chroma_persist_directory
        self._use_semantic_retrieval = use_semantic_retrieval

    @property
    def has_llm(self) -> bool:
        return self._llm_client_factory is not None

    @cached_property
    def llm_client(self) -> LLMClient:
        if self._llm_client_factory is None:
            raise RuntimeError("No LLM configured; set GROQ_API_KEY.")
        return self._llm_client_factory()

    @cached_property
    def retrieval(self) -> RetrievalContainer:
        from src.infrastructure.containers.retrieval_container import RetrievalContainer

        kwargs: dict[str, object] = {"embedding_provider": self._embedding_provider}
        if self._chroma_persist_directory is not None:
            kwargs["persist_directory"] = self._chroma_persist_directory
        return RetrievalContainer(**kwargs)  # type: ignore[arg-type]

    @cached_property
    def evaluation(self) -> EvaluationContainer:
        from src.infrastructure.containers.evaluation_container import EvaluationContainer

        factory = (lambda: self.llm_client) if self.has_llm else None
        return EvaluationContainer(llm_client_factory=factory)

    @cached_property
    def cv(self) -> CVContainer:
        from src.infrastructure.containers.cv_container import CVContainer

        return CVContainer(
            llm_client=self.llm_client,
        )

    @cached_property
    def interview_session_service(self) -> InterviewSessionService:
        from src.application.services.interview_session_service import (
            InterviewSessionService,
        )
        from src.infrastructure.repositories.json_question_repository_builder import (
            JsonQuestionRepositoryBuilder,
        )
        from src.services.weighted_scoring_engine import WeightedScoringEngine

        retriever = None
        if self._use_semantic_retrieval:
            # Resolved on first use, so the embedding model loads lazily and
            # a load failure only disables retrieval (see the service).
            def retriever(*, query, context, top_k):  # type: ignore[no-untyped-def]
                return [
                    result.question
                    for result in self.question_retrieval_service.retrieve(
                        query=query, context=context, top_k=top_k
                    )
                ]

        return InterviewSessionService(
            question_repository=JsonQuestionRepositoryBuilder.build_default(
                file_path=self._question_bank_path,
            ),
            scoring_engine=WeightedScoringEngine(),
            evaluator=self.evaluation.evaluator,
            retriever=retriever,
        )

    @property
    def answer_evaluation_service(self) -> AnswerEvaluationService:
        return self.evaluation.answer_evaluation_service

    @property
    def adaptive_selection_service(self) -> AdaptiveQuestionSelectionService:
        return self.retrieval.adaptive_selection_service

    @property
    def question_retrieval_service(self) -> SemanticQuestionRetrievalService:
        return self.retrieval.question_retrieval_service

    @property
    def cv_analysis_orchestration_service(self) -> CVAnalysisOrchestrationService:
        return self.cv.cv_analysis_orchestration_service
