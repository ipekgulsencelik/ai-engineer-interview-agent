from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.constants.chroma_question import (
    CURRENT_QUESTION_METADATA_VERSION,
)
from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    EXPECTED_POINTS_METADATA_KEY,
    FOLLOWUP_ALLOWED_METADATA_KEY,
    FOLLOWUP_METADATA_KEY,
    IDEAL_ANSWER_HINT_METADATA_KEY,
    KEYWORDS_METADATA_KEY,
    LEVEL_METADATA_KEY,
    MARKET_WEIGHT_METADATA_KEY,
    QUESTION_ID_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
    TEXT_METADATA_KEY,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    QuestionVectorMetadata,
)


class QuestionVectorMetadataMapper:
    """
    Maps Question entities to Chroma-safe metadata payloads.

    The payload carries every field ChromaQuestionResultMapper needs to
    rehydrate the full Question, so search results are self-contained.
    Empty lists are omitted because Chroma rejects empty-list metadata.
    """

    @classmethod
    def from_question(
        cls,
        *,
        question: Question,
    ) -> QuestionVectorMetadata:
        metadata: QuestionVectorMetadata = {
            "metadata_version": CURRENT_QUESTION_METADATA_VERSION,
            QUESTION_ID_METADATA_KEY: question.id,
            TEXT_METADATA_KEY: question.text,
            CATEGORY_METADATA_KEY: cls._to_value(question.category),
            LEVEL_METADATA_KEY: cls._to_value(question.level),
            DIFFICULTY_METADATA_KEY: question.difficulty,
            QUESTION_TYPE_METADATA_KEY: cls._to_value(question.question_type),
            MARKET_WEIGHT_METADATA_KEY: question.market_weight,
            FOLLOWUP_ALLOWED_METADATA_KEY: question.followup_allowed,
            EXPECTED_POINTS_METADATA_KEY: list(question.expected_points) or None,
            KEYWORDS_METADATA_KEY: list(question.keywords) or None,
            FOLLOWUP_METADATA_KEY: question.followup,
            IDEAL_ANSWER_HINT_METADATA_KEY: question.ideal_answer_hint,
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
