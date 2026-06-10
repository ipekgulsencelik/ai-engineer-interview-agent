from __future__ import annotations

from src.infrastructure.errors.vector_store_error import (
    VectorStoreError,
)
from src.infrastructure.schemas.chroma_question_vector_store_schema import (
    CHROMA_QUESTION_VECTOR_STORE_SCHEMA,
)


class ChromaQuestionVectorStoreValidator:
    """
    ChromaQuestionVectorStore input validation helper.
    """

    @classmethod
    def validate_index_inputs(
        cls,
        *,
        questions: object,
        embeddings: object,
    ) -> None:
        cls._validate_list_field(
            field_name="questions",
            value=questions,
        )
        cls._validate_list_field(
            field_name="embeddings",
            value=embeddings,
        )

        if len(questions) != len(embeddings):
            raise VectorStoreError(
                "Questions and embeddings count mismatch."
            )

        for question in questions:
            cls._validate_item_type(
                field_name="questions",
                value=question,
            )

        for embedding in embeddings:
            cls.validate_embedding(
                embedding=embedding,
            )

    @classmethod
    def validate_embedding(
        cls,
        *,
        embedding: object,
    ) -> None:
        cls._validate_list_field(
            field_name="embedding",
            value=embedding,
        )

        for value in embedding:
            if isinstance(value, bool):
                raise VectorStoreError(
                    "embedding must not contain boolean values."
                )

            if not isinstance(
                value,
                CHROMA_QUESTION_VECTOR_STORE_SCHEMA[
                    "embedding"
                ]["item_type"],
            ):
                raise VectorStoreError(
                    "embedding must contain only numeric values."
                )

    @classmethod
    def validate_search_inputs(
        cls,
        *,
        query_embedding: object,
        top_k: object,
    ) -> None:
        cls.validate_embedding(
            embedding=query_embedding,
        )

        rules = CHROMA_QUESTION_VECTOR_STORE_SCHEMA[
            "top_k"
        ]

        if rules.get("allow_bool") is False and isinstance(top_k, bool):
            raise VectorStoreError(
                "top_k must not be a boolean."
            )

        if not isinstance(top_k, rules["type"]):
            raise VectorStoreError(
                "top_k must be an integer."
            )

        if top_k < rules["min_value"]:
            raise VectorStoreError(
                "top_k must be greater than zero."
            )

    @staticmethod
    def _validate_list_field(
        *,
        field_name: str,
        value: object,
    ) -> None:
        rules = CHROMA_QUESTION_VECTOR_STORE_SCHEMA[
            field_name
        ]

        if not isinstance(value, rules["type"]):
            raise VectorStoreError(
                f"{field_name} must be a list."
            )

        if (
            rules.get("allow_empty") is False
            and not value
        ):
            raise VectorStoreError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_item_type(
        *,
        field_name: str,
        value: object,
    ) -> None:
        rules = CHROMA_QUESTION_VECTOR_STORE_SCHEMA[
            field_name
        ]

        item_type = rules.get("item_type")

        if item_type is not None and not isinstance(value, item_type):
            raise VectorStoreError(
                f"{field_name} has invalid item type."
            )