from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeAlias

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)


JsonData: TypeAlias = Any


class JsonFileParser:
    """
    JSON file parser.
    """

    @staticmethod
    def parse(
        *,
        file_path: Path,
    ) -> JsonData:
        if not file_path.exists():
            raise EvaluationDatasetLoadingError(
                f"JSON file does not exist: {file_path}"
            )

        if not file_path.is_file():
            raise EvaluationDatasetLoadingError(
                f"Path is not a file: {file_path}"
            )

        try:
            with file_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise EvaluationDatasetLoadingError(
                f"Invalid JSON file: {file_path}"
            ) from exc
        except OSError as exc:
            raise EvaluationDatasetLoadingError(
                f"Could not read JSON file: {file_path}"
            ) from exc