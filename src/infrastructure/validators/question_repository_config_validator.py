from __future__ import annotations

from pathlib import Path

from src.infrastructure.errors.question_repository_config_error import (
    QuestionRepositoryConfigError,
)
from src.infrastructure.schemas.question_repository_config_schema import (
    QUESTION_REPOSITORY_CONFIG_SCHEMA,
)


class QuestionRepositoryConfigValidator:
    """
    Repository configuration validation helper.
    """

    @staticmethod
    def validate_file_path(
        file_path: str | Path,
    ) -> None:
        schema = QUESTION_REPOSITORY_CONFIG_SCHEMA["file_path"]

        if not isinstance(file_path, schema["type"]):
            raise QuestionRepositoryConfigError(
                "file_path must be str or Path."
            )

        if schema.get("non_empty", False) and not str(file_path).strip():
            raise QuestionRepositoryConfigError(
                "file_path cannot be empty."
            )

        if schema.get("strip", False) and str(file_path) != str(file_path).strip():
            raise QuestionRepositoryConfigError(
                "file_path cannot have leading or trailing whitespace."
            )

        if len(str(file_path)) > 255:
            raise QuestionRepositoryConfigError(
                "file_path cannot exceed 255 characters."
            )

        if not Path(str(file_path).strip()).exists():
            raise QuestionRepositoryConfigError(
                f"File not found: {str(file_path).strip()}"
            )

        if not Path(str(file_path).strip()).is_file():
            raise QuestionRepositoryConfigError(
                f"Path is not a file: {str(file_path).strip()}"
            )