from __future__ import annotations

from functools import cached_property

from src.application.ports.question_vector_store import QuestionVectorStore
from src.application.services.adaptive_question_selection_service import (
    AdaptiveQuestionSelectionService,
)
from src.application.services.question_ranking_service import QuestionRankingService
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)
from src.config.settings import settings
from src.infrastructure.constants.embedding_defaults import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_NORMALIZE_EMBEDDINGS,
    DEFAULT_RETRY_BACKOFF_SECONDS,
    DEFAULT_RETRY_COUNT,
)
from src.infrastructure.containers.base_container import BaseContainer
from src.infrastructure.embedding.embedding_retry_executor import (
    EmbeddingRetryExecutor,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.embedding.sentence_transformer_model_loader import (
    SentenceTransformerModelLoader,
)
from src.infrastructure.vector_stores.sqlite.sqlite_question_vector_store import (
    SqliteQuestionVectorStore,
)


class RetrievalContainer(BaseContainer):
    """
    Retrieval dependency container.
    """

    @cached_property
    def embedding_provider(
        self,
    ) -> SentenceTransformerEmbeddingProvider:
        return SentenceTransformerEmbeddingProvider(
            model=SentenceTransformerModelLoader.load(
                model_name=settings.EMBEDDING_MODEL_NAME,
            ),
            retry_executor=EmbeddingRetryExecutor(
                retry_count=DEFAULT_RETRY_COUNT,
                retry_backoff_seconds=DEFAULT_RETRY_BACKOFF_SECONDS,
            ),
            normalize_embeddings=DEFAULT_NORMALIZE_EMBEDDINGS,
            batch_size=DEFAULT_BATCH_SIZE,
        )

    @cached_property
    def vector_store(
        self,
    ) -> QuestionVectorStore:
        return SqliteQuestionVectorStore(
            database_path=settings.QUESTION_VECTOR_DB_PATH,
        )

    @cached_property
    def question_retrieval_service(
        self,
    ) -> SemanticQuestionRetrievalService:
        return SemanticQuestionRetrievalService(
            embedding_provider=self.embedding_provider,
            vector_store=self.vector_store,
        )

    @cached_property
    def question_ranking_service(
        self,
    ) -> QuestionRankingService:
        return QuestionRankingService()

    @cached_property
    def adaptive_selection_service(
        self,
    ) -> AdaptiveQuestionSelectionService:
        return AdaptiveQuestionSelectionService(
            retrieval_service=self.question_retrieval_service,
            ranking_service=self.question_ranking_service,
        )