from __future__ import annotations

from pathlib import Path

from src.application.services.adaptive_question_selection_service import (
    AdaptiveQuestionSelectionService,
)
from src.application.services.question_ranking_service import (
    QuestionRankingService,
)
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)
from src.application.use_cases.load_question_bank_use_case import (
    LoadQuestionBankUseCase,
)
from src.infrastructure.embeddings.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)
from src.infrastructure.vector_store.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)
from src.infrastructure.config.app_paths import (
    DEFAULT_QUESTION_BANK_PATH,
)


class ServiceContainer:
    """
    Application dependency composition container.
    """

    def __init__(
        self,
        *,
        question_bank_path: Path | None = None,
    ) -> None:
        self._question_bank_path = (
            question_bank_path
            or DEFAULT_QUESTION_BANK_PATH
        )

        self._embedding_model = SentenceTransformerEmbeddingModel()
        self._vector_store = ChromaQuestionVectorStore()

        self._retrieval_service = SemanticQuestionRetrievalService(
            embedding_model=self._embedding_model,
            vector_store=self._vector_store,
        )

        self._ranking_service = QuestionRankingService()

        self._adaptive_selection_service = AdaptiveQuestionSelectionService(
            retrieval_service=self._retrieval_service,
            ranking_service=self._ranking_service,
        )

    def adaptive_selection_service(
        self,
    ) -> AdaptiveQuestionSelectionService:
        return self._adaptive_selection_service

    def load_question_bank_use_case(
        self,
    ) -> LoadQuestionBankUseCase:
        repository = JsonQuestionRepository(
            file_path=self._question_bank_path,
        )

        return LoadQuestionBankUseCase(
            question_repository=repository,
        )