from __future__ import annotations

from typing import Any

from src.application.validators.question_metadata_required_keys_validator import (
    QuestionMetadataRequiredKeysValidator,
)
from src.application.validators.question_rehydration_input_validator import (
    QuestionRehydrationInputValidator,
)


class QuestionMetadataRehydrationValidator:
    """
    Persisted question metadata validation facade.
    """

    @staticmethod
    def validate(
        *,
        question_id: str,
        metadata: dict[str, Any],
    ) -> None:
        QuestionRehydrationInputValidator.validate_question_id(
            question_id=question_id,
        )

        QuestionRehydrationInputValidator.validate_metadata(
            metadata=metadata,
        )

        QuestionMetadataRequiredKeysValidator.validate(
            metadata=metadata,
        )