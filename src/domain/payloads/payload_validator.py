from __future__ import annotations

from src.domain.errors.question_validation_error import (
    QuestionValidationError,
)


class PayloadValidator:
    """
    Raw payload shape validation helper.
    """

    @staticmethod
    def validate_dict_payload(
        *,
        payload: object,
    ) -> None:
        if not isinstance(payload, dict):
            raise QuestionValidationError(
                "Question payload must be a dictionary."
            )

    @staticmethod
    def validate_required_key(
        *,
        payload: dict[str, object],
        key: str,
    ) -> None:
        if key not in payload:
            raise QuestionValidationError(
                f"Missing required field: {key}."
            )