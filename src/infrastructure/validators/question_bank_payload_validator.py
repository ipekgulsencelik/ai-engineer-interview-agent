from __future__ import annotations

from typing import Any, Mapping

from src.infrastructure.errors.question_bank_file_error import (
    QuestionBankFileError,
)


class QuestionBankPayloadValidator:
    """
    Question bank payload validation helper.
    """

    @staticmethod
    def validate_and_return_items(
        *,
        payload: Any,
    ) -> list[Mapping[str, Any]]:
        if not isinstance(payload, list):
            raise QuestionBankFileError(
                "Question bank JSON root must be a list."
            )

        items: list[Mapping[str, Any]] = []

        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                raise QuestionBankFileError(
                    f"Question payload at index "
                    f"{index} must be a dictionary."
                )

            items.append(item)

        return items