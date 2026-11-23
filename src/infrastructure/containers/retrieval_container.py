from __future__ import annotations

from functools import cached_property

from src.application.ports.embedding_provider import (
    EmbeddingProvider,
)
from src.application.ports.question_vector_store import (
    QuestionVectorStore,
)
from src.application.services.adaptive_question_selection_service import (
    AdaptiveQuestionSelectionService,
)
from src.application.services.question_ranking_service import (
    QuestionRankingService,
)
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)
from src.infrastructure.constants.chroma_defaults import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
)
from src.infrastructure.containers.base_container import (
    BaseContainer,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider_factory import (
    DEFAULT_EMBEDDING_MODEL_NAME,
    SentenceTransformerEmbeddingProviderFactory,
)
from src.infrastructure.vector_stores.chroma.chroma_question_vector_store_builder import (
    ChromaQuestionVectorStoreBuilder,
)


class RetrievalContainer(BaseContainer):
    """
    Retrieval dependency container.

    Defaults read the persisted Chroma index built by
    `python -m src.scripts.index_question_bank`. Pass embedding_provider or
    vector_store to override (e.g. offline tests).
    """

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider | None = None,
        vector_store: QuestionVectorStore | None = None,
        persist_directory: str = DEFAULT_CHROMA_PERSIST_DIRECTORY,
        collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
        embedding_model_name: str = DEFAULT_EMBEDDING_MODEL_NAME,
    ) -> None:
        self._embedding_provider_override = embedding_provider
        self._vector_store_override = vector_store
        self._persist_directory = persist_directory
        self._collection_name = collection_name
        self._embedding_model_name = embedding_model_name

    @cached_property
    def embedding_provider(
        self,
    ) -> EmbeddingProvider:
        if self._embedding_provider_override is not None:
            return self._embedding_provider_override
        return SentenceTransformerEmbeddingProviderFactory.build(
            model_name=self._embedding_model_name,
        )

    @cached_property
    def vector_store(
        self,
    ) -> QuestionVectorStore:
        if self._vector_store_override is not None:
            return self._vector_store_override
        return ChromaQuestionVectorStoreBuilder.build_default(
            persist_directory=self._persist_directory,
            collection_name=self._collection_name,
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
