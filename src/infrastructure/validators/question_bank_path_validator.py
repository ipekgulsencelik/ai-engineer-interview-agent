from __future__ import annotations

from pathlib import Path

from src.infrastructure.errors.question_bank_path_error import (
    QuestionBankPathError,
)
from src.infrastructure.schemas.question_bank_path_schema import (
    QUESTION_BANK_PATH_SCHEMA,
)


class QuestionBankPathValidator:
    """
    Question bank path validation helper.
    """

    @staticmethod
    def validate_file_path(
        *,
        file_path: Path,
    ) -> None:
        schema = QUESTION_BANK_PATH_SCHEMA["file_path"]

        if not isinstance(
            file_path,
            schema["type"],
        ):
            raise QuestionBankPathError(
                "file_path must be a Path instance."
            )

        normalized_path = str(file_path).strip()

        if (
            schema.get("non_empty", False)
            and not normalized_path
        ):
            raise QuestionBankPathError(
                "file_path cannot be empty."
            )

        if not file_path.exists():
            raise QuestionBankPathError(
                f"Question bank file does not exist: "
                f"{file_path}"
            )

        if not file_path.is_file():
            raise QuestionBankPathError(
                f"Question bank path is not a file: "
                f"{file_path}"
            )
            
        if len(normalized_path) > 255:
            raise QuestionBankPathError(
                "file_path cannot exceed 255 characters."
            )

