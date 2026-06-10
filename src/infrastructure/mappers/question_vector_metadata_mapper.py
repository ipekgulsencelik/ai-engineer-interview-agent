from __future__ import annotations

from typing import Any

from src.domain.entities.question import Question
from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    FOLLOWUP_ALLOWED_METADATA_KEY,
    LEVEL_METADATA_KEY,
    MARKET_WEIGHT_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
)


class QuestionVectorMetadataMapper:
    """
    Question entity -> vector store metadata mapper.
    """

    @staticmethod
    def to_metadata(
        *,
        question: Question,
    ) -> dict[str, Any]:
        return {
            CATEGORY_METADATA_KEY: question.category.value,
            LEVEL_METADATA_KEY: question.level.value,
            QUESTION_TYPE_METADATA_KEY: (
                question.question_type.value
            ),
            DIFFICULTY_METADATA_KEY: (
                question.difficulty
            ),
            MARKET_WEIGHT_METADATA_KEY: (
                question.market_weight
            ),
            FOLLOWUP_ALLOWED_METADATA_KEY: (
                question.followup_allowed
            ),
        }