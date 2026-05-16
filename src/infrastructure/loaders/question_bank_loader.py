from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from src.infrastructure.path_resolvers.question_bank_path_resolver import (
    QuestionBankPathResolver,
)
from src.infrastructure.readers.json_file_reader import (
    JsonFileReader,
)
from src.infrastructure.validators.question_bank_file_validator import (
    QuestionBankFileValidator,
)
from src.infrastructure.validators.question_bank_payload_validator import (
    QuestionBankPayloadValidator,
)


class QuestionBankLoader:
    """
    JSON question bank loader.
    """

    def __init__(
        self,
        *,
        file_path: Path,
        path_resolver: QuestionBankPathResolver,
        json_reader: JsonFileReader,
    ) -> None:
        self._file_path = file_path
        self._path_resolver = path_resolver
        self._json_reader = json_reader

    def exists(self) -> bool:
        return self._resolve_path().exists()

    def load_items(self) -> list[Mapping[str, Any]]:
        resolved_path = self._resolve_path()

        QuestionBankFileValidator.validate_exists(
            file_path=resolved_path,
            original_path=self._file_path,
        )

        QuestionBankFileValidator.validate_is_file(
            file_path=resolved_path,
        )

        raw_payload = self._json_reader.read(
            file_path=resolved_path,
        )

        return QuestionBankPayloadValidator.validate_and_return_items(
            payload=raw_payload,
        )

    def _resolve_path(self) -> Path:
        return self._path_resolver.resolve(
            file_path=self._file_path,
        )