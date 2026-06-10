from __future__ import annotations

from functools import cached_property

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
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
)
from src.infrastructure.containers.base_container import (
    BaseContainer,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.vector_stores.chroma.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)


class RetrievalContainer(BaseContainer):
    """
    Retrieval dependency container.
    """

    @cached_property
    def embedding_provider(
        self,
    ) -> SentenceTransformerEmbeddingProvider:
        return SentenceTransformerEmbeddingProvider()

    @cached_property
    def vector_store(
        self,
    ) -> ChromaQuestionVectorStore:
        return ChromaQuestionVectorStore(
            persist_directory=DEFAULT_CHROMA_PERSIST_DIRECTORY,
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