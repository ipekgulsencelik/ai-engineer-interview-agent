from __future__ import annotations

from pathlib import Path

from src.infrastructure.constants.question_bank_paths import (
    QUESTION_BANK_FALLBACK_PATHS,
)


class QuestionBankPathResolver:
    """
    Question bank file path resolution policy.
    """

    def resolve(
        self,
        *,
        file_path: Path,
    ) -> Path:
        if file_path.exists():
            return file_path

        fallback_path = self._resolve_fallback_path(
            file_path=file_path,
        )

        if (
            fallback_path is not None
            and fallback_path.exists()
        ):
            return fallback_path

        return file_path

    @staticmethod
    def _resolve_fallback_path(
        *,
        file_path: Path,
    ) -> Path | None:
        return QUESTION_BANK_FALLBACK_PATHS.get(
            file_path.as_posix(),
        )