from __future__ import annotations

from src.application.ports.question_vector_store import QuestionVectorStore
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.infrastructure.vector_stores.question_chroma.chroma_client_factory import (
    create_chroma_client,
)
from src.infrastructure.vector_stores.question_chroma.chroma_protocols import (
    ChromaClientProtocol,
)
from src.infrastructure.vector_stores.question_chroma.chroma_question_query_builder import (
    ChromaQuestionQueryBuilder,
)
from src.infrastructure.mappers.chroma_question_result_mapper import (
    ChromaQuestionResultMapper,
)
from src.infrastructure.validators.chroma_question_vector_store_validator import (
    ChromaQuestionVectorStoreValidator,
)


class ChromaQuestionVectorStore(QuestionVectorStore):
    """ChromaDB-backed semantic question vector store."""

    def __init__(
        self,
        *,
        persist_directory: str,
        collection_name: str = "questions",
        client: ChromaClientProtocol | None = None,
    ) -> None:
        ChromaQuestionVectorStoreValidator.validate_init(
            persist_directory=persist_directory,
            collection_name=collection_name,
        )

        self._client = client or create_chroma_client(
            persist_directory=persist_directory,
        )
        self._collection = self._client.get_or_create_collection(name=collection_name)


    def add_question(
        self,
        *,
        question: Question,
        embedding: list[float],
    ) -> None:
        ChromaQuestionVectorStoreValidator.validate_add_question(
            question=question,
            embedding=embedding,
        )

        self._collection.upsert(
            ids=[question.id],
            embeddings=[embedding],
            documents=[question.text],
            metadatas=[
                {
                    "question_id": question.id,
                    "text": question.text,
                    "category": question.category.value,
                    "level": question.level.value,
                    "difficulty": question.difficulty.value,
                    "question_type": question.question_type.value,
                    "expected_points": question.expected_points,
                    "keywords": question.keywords,
                    "market_weight": question.market_weight,
                    "followup_allowed": question.followup_allowed,
                }
            ],
        )


    def search_questions(
        self,
        *,
        embedding: list[float],
        top_k: int,
        level: Level,
    ) -> list[Question]:
        ChromaQuestionVectorStoreValidator.validate_search(
            embedding=embedding,
            top_k=top_k,
            level=level,
        )

        payload = ChromaQuestionQueryBuilder.build(
            embedding=embedding,
            top_k=top_k,
            level=level,
        )
        results = self._collection.query(**payload)
        return ChromaQuestionResultMapper.to_questions(results)
