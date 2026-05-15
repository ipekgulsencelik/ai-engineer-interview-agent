from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.infrastructure.validators.question_bank_loader_validator import (
    QuestionBankLoaderValidator,
)


class QuestionBankLoader:
    """Loads raw question records from a JSON question bank file."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def exists(self) -> bool:
        return self._resolve_existing_path().exists()

    def load_items(self) -> list[dict[str, Any]]:
        if not self.exists():
            raise FileNotFoundError(f"Question bank file not found: {self._file_path}")

        resolved_path = self._resolve_existing_path()

        if not resolved_path.exists():
            raise FileNotFoundError(f"Question bank file not found: {self._file_path}")

        with resolved_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        QuestionBankLoaderValidator.validate_payload(data)

        return data

    def _resolve_existing_path(self) -> Path:
        if self._file_path.exists():
            return self._file_path

        if self._file_path.as_posix() == "data/questions.json":
            fallback = Path("data/question_bank/questions.json")
            if fallback.exists():
                return fallback

        return self._file_path