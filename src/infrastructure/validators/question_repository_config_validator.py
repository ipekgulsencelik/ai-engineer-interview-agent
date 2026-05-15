from __future__ import annotations

from pathlib import Path


class QuestionRepositoryConfigValidator:
    """Validation helpers for repository construction/configuration."""

    @staticmethod
    def validate_file_path(file_path: str | Path) -> None:
        if not isinstance(file_path, (str, Path)):
            raise ValueError("file_path must be a string or Path.")

        if isinstance(file_path, str) and not file_path.strip():
            raise ValueError("file_path cannot be empty.")

        if not Path(file_path.strip()).exists():
            raise FileNotFoundError(f"File not found: {file_path.strip()}")

        if isinstance(file_path, str) and len(file_path) > 255:
            raise ValueError("file_path cannot exceed 255 characters.")