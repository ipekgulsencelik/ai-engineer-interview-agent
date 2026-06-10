from __future__ import annotations

from src.domain.entities.question import Question
from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    FOLLOWUP_ALLOWED_METADATA_KEY,
    LEVEL_METADATA_KEY,
    MARKET_WEIGHT_METADATA_KEY,
    QUESTION_ID_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    QuestionVectorMetadata,
)


class QuestionVectorMetadataMapper:
    """
    Maps Question entities to Chroma-safe metadata payloads.
    """

    @classmethod
    def from_question(
        cls,
        *,
        question: Question,
    ) -> QuestionVectorMetadata:
        metadata: QuestionVectorMetadata = {
            QUESTION_ID_METADATA_KEY: question.id,
            CATEGORY_METADATA_KEY: cls._to_value(question.category),
            LEVEL_METADATA_KEY: cls._to_value(question.level),
            DIFFICULTY_METADATA_KEY: question.difficulty,
            QUESTION_TYPE_METADATA_KEY: cls._to_value(question.question_type),
            MARKET_WEIGHT_METADATA_KEY: question.market_weight,
            FOLLOWUP_ALLOWED_METADATA_KEY: question.followup_allowed,
        }

        return cls._remove_none_values(metadata=metadata)

    @staticmethod
    def _to_value(
        value: object,
    ) -> object:
        if hasattr(value, "value"):
            return value.value

        return value

    @staticmethod
    def _remove_none_values(
        *,
        metadata: QuestionVectorMetadata,
    ) -> QuestionVectorMetadata:
        return {
            key: value
            for key, value in metadata.items()
            if value is not None
        }
