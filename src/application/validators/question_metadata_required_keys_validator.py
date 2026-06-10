from __future__ import annotations

from typing import Any

from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    LEVEL_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
    TEXT_METADATA_KEY,
)
from src.application.errors.question_rehydration_error import (
    QuestionRehydrationError,
)


class QuestionMetadataRequiredKeysValidator:
    """
    Required metadata key validation helper.
    """

    _REQUIRED_KEYS: tuple[str, ...] = (
        TEXT_METADATA_KEY,
        CATEGORY_METADATA_KEY,
        LEVEL_METADATA_KEY,
        DIFFICULTY_METADATA_KEY,
        QUESTION_TYPE_METADATA_KEY,
    )

    @classmethod
    def validate(
        cls,
        *,
        metadata: dict[str, Any],
    ) -> None:
        for key in cls._REQUIRED_KEYS:
            if key not in metadata:
                raise QuestionRehydrationError(
                    f"Missing required question metadata key: {key}."
                )