from __future__ import annotations

from src.application.ports.question_vector_store import (
    QuestionVectorStore,
)
from src.domain.entities.question import Question
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.domain.retrieval.search_filters import (
    SearchFilters,
)
from src.infrastructure.errors.vector_store_error import (
    VectorStoreError,
)
from src.infrastructure.mappers.chroma_metadata_mapper import (
    ChromaMetadataMapper,
)
from src.infrastructure.mappers.chroma_question_search_result_mapper import (
    ChromaQuestionSearchResultMapper,
)
from src.infrastructure.validators.chroma_question_vector_store_validator import (
    ChromaQuestionVectorStoreValidator,
)
from src.infrastructure.vector_stores.chroma.chroma_protocols import (
    ChromaCollectionProtocol,
)
from src.infrastructure.vector_stores.chroma.chroma_question_query_builder import (
    ChromaQuestionQueryBuilder,
)


class ChromaQuestionVectorStore(QuestionVectorStore):
    """
    ChromaDB-backed semantic question vector store.
    """

    def __init__(
        self,
        *,
        collection: ChromaCollectionProtocol,
        result_mapper: ChromaQuestionSearchResultMapper | None = None,
    ) -> None:
        self._collection = collection
        self._result_mapper = (
            result_mapper
            or ChromaQuestionSearchResultMapper()
        )

    def index_questions(
        self,
        *,
        questions: list[Question],
        embeddings: list[list[float]],
    ) -> None:
        ChromaQuestionVectorStoreValidator.validate_index_inputs(
            questions=questions,
            embeddings=embeddings,
        )

        try:
            self._collection.upsert(
                ids=[question.id for question in questions],
                embeddings=embeddings,
                documents=[question.text for question in questions],
                metadatas=[
                    ChromaMetadataMapper.from_question(
                        question=question,
                    )
                    for question in questions
                ],
            )
        except Exception as exc:
            raise VectorStoreError(
                "Failed to index questions into Chroma."
            ) from exc

    def add_question(
        self,
        *,
        question: Question,
        embedding: list[float],
    ) -> None:
        self.index_questions(
            questions=[question],
            embeddings=[embedding],
        )

    def search_questions(
        self,
        *,
        query_embedding: list[float],
        top_k: int,
        filters: SearchFilters | None = None,
    ) -> list[QuestionSearchResult]:
        ChromaQuestionVectorStoreValidator.validate_search_inputs(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters,
        )

        payload = ChromaQuestionQueryBuilder.build(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters,
        )

        try:
            results = self._collection.query(**payload)
        except Exception as exc:
            raise VectorStoreError(
                "Failed to search questions in Chroma."
            ) from exc

        return self._result_mapper.to_results(
            results=results,
        )