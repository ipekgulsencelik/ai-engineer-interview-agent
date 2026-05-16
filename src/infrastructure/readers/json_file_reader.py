from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.infrastructure.errors.json_file_read_error import (
    JsonFileReadError,
)


class JsonFileReader:
    """
    JSON file reader.

    Sadece JSON dosyası okuma sorumluluğu taşır.
    """

    @staticmethod
    def read(
        *,
        file_path: Path,
    ) -> Any:
        try:
            with file_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except json.JSONDecodeError as exc:
            raise JsonFileReadError(
                f"Invalid JSON content in file: {file_path}"
            ) from exc