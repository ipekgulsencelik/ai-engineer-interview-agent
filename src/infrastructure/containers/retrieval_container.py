from __future__ import annotations

from functools import cached_property

from src.application.services.question_retrieval_service import (
    QuestionRetrievalService,
)
from src.infrastructure.constants.vector_store import (
    CHROMA_PERSIST_DIRECTORY,
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
            persist_directory=CHROMA_PERSIST_DIRECTORY,
        )

    @cached_property
    def question_retrieval_service(
        self,
    ) -> QuestionRetrievalService:
        return QuestionRetrievalService(
            embedding_provider=self.embedding_provider,
            vector_store=self.vector_store,
        )