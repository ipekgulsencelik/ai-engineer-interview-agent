from __future__ import annotations

import pytest

from src.domain.enums.level import Level
from src.domain.constants.chroma_question import (
    REQUIRED_QUESTION_METADATA_FIELDS,
)
from src.infrastructure.validations.chroma_question_metadata_schema import (
    CHROMA_QUESTION_METADATA_SCHEMA,
)
from src.infrastructure.vector_stores.question_chroma.chroma_question_query_builder import (
    ChromaQuestionQueryBuilder,
)
from src.infrastructure.vector_stores.question_chroma.chroma_question_result_mapper import (
    ChromaQuestionResultMapper,
)
from src.infrastructure.vector_stores.question_chroma.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)
from src.infrastructure.validators.chroma_question_vector_store_validator import (
    ChromaQuestionVectorStoreValidator,
)


class _FakeCollection:
    def __init__(self) -> None:
        self.last_payload = None

    def query(self, **kwargs):
        self.last_payload = kwargs
        return {"metadatas": [[]]}


class _FakeClient:
    def __init__(self, collection: _FakeCollection) -> None:
        self.collection = collection
        self.collection_name = None

    def get_or_create_collection(self, *, name: str) -> _FakeCollection:
        self.collection_name = name
        return self.collection


def test_query_builder_builds_level_filtered_payload() -> None:
    payload = ChromaQuestionQueryBuilder.build(
        embedding=[0.1, 0.2],
        top_k=3,
        level=Level.JR,
    )

    assert payload == {
        "query_embeddings": [[0.1, 0.2]],
        "n_results": 3,
        "where": {"level": Level.JR.value},
    }


def test_validator_rejects_invalid_top_k() -> None:
    with pytest.raises(ValueError, match="top_k"):
        ChromaQuestionVectorStoreValidator.validate_search(
            embedding=[0.1],
            top_k=0,
            level=Level.JR,
        )


def test_mapper_rejects_missing_required_fields() -> None:
    with pytest.raises(ValueError, match="Missing required metadata fields"):
        ChromaQuestionResultMapper.to_questions(
            {"metadatas": [[{"id": "q-1", "text": "x"}]]}
        )


def test_store_delegates_query_and_returns_mapped_questions() -> None:
    collection = _FakeCollection()
    client = _FakeClient(collection)

    store = ChromaQuestionVectorStore(
        persist_directory="/tmp/chroma",
        collection_name="questions",
        client=client,
    )

    result = store.search_questions(
        embedding=[0.5, 0.6],
        top_k=2,
        level=Level.JR,
    )

    assert result == []
    assert client.collection_name == "questions"
    assert collection.last_payload == {
        "query_embeddings": [[0.5, 0.6]],
        "n_results": 2,
        "where": {"level": "JR"},
    }


def test_validator_rejects_non_finite_embedding_values() -> None:
    with pytest.raises(ValueError, match="finite"):
        ChromaQuestionVectorStoreValidator.validate_search(
            embedding=[0.1, float("inf")],
            top_k=1,
            level=Level.JR,
        )


def test_mapper_returns_empty_list_when_metadata_batches_missing() -> None:
    assert ChromaQuestionResultMapper.to_questions({}) == []


def test_mapper_rejects_invalid_metadata_field_type() -> None:
    with pytest.raises(TypeError, match="Invalid type"):
        ChromaQuestionResultMapper.to_questions(
            {
                "metadatas": [[{
                    "id": "q-1",
                    "text": "question",
                    "category": "system_design",
                    "level": "JR",
                    "difficulty": 1,
                    "question_type": "conceptual",
                    "keywords": "should-be-list",
                }]]
            }
        )


def test_schema_contains_all_required_metadata_fields() -> None:
    schema_required = {
        field
        for field, rules in CHROMA_QUESTION_METADATA_SCHEMA.items()
        if rules.get("required")
    }
    assert schema_required == set(REQUIRED_QUESTION_METADATA_FIELDS)


def test_mapper_accepts_supported_metadata_version() -> None:
    question_list = ChromaQuestionResultMapper.to_questions(
        {
            "metadatas": [[{
                "id": "q-1",
                "text": "question",
                "category": "system_design",
                "level": "JR",
                "difficulty": 1,
                "question_type": "conceptual",
                "metadata_version": "v1",
            }]]
        }
    )
    assert len(question_list) == 1


def test_mapper_rejects_unsupported_metadata_version() -> None:
    with pytest.raises(ValueError, match="Unsupported metadata_version"):
        ChromaQuestionResultMapper.to_questions(
            {
                "metadatas": [[{
                    "id": "q-1",
                    "text": "question",
                    "category": "system_design",
                    "level": "JR",
                    "difficulty": 1,
                    "question_type": "conceptual",
                    "metadata_version": "v2",
                }]]
            }
        )
