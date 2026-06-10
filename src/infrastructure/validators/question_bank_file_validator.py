from __future__ import annotations

from pathlib import Path

from src.infrastructure.errors.question_bank_file_error import (
    QuestionBankFileError,
)


class QuestionBankFileValidator:
    """
    Question bank file validation helper.
    """

    @staticmethod
    def validate_exists(
        *,
        file_path: Path,
        original_path: Path,
    ) -> None:
        if not file_path.exists():
            raise QuestionBankFileError(
                f"Question bank file not found: {original_path}"
            )

    @staticmethod
    def validate_is_file(
        *,
        file_path: Path,
    ) -> None:
        if not file_path.is_file():
            raise QuestionBankFileError(
                f"Question bank path is not a file: {file_path}"
            )