from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BenchmarkHistoryEntry:
    """
    Immutable benchmark history entry.

    Stores the lightweight result data needed by evaluation ops
    histories without requiring a full experiment snapshot payload.
    """

    experiment_id: str
    benchmark_id: str
    benchmark_version: str
    overall_score: float
    model_name: str
    recorded_at: datetime
    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        self._validate_non_empty_string(
            value=self.experiment_id,
            field_name="experiment_id",
        )
        self._validate_non_empty_string(
            value=self.benchmark_id,
            field_name="benchmark_id",
        )
        self._validate_non_empty_string(
            value=self.benchmark_version,
            field_name="benchmark_version",
        )
        self._validate_non_empty_string(
            value=self.model_name,
            field_name="model_name",
        )

        if not isinstance(self.overall_score, (int, float)) or isinstance(
            self.overall_score,
            bool,
        ):
            raise EvaluationValidationError(
                "overall_score must be numeric."
            )

        if self.overall_score < 0 or self.overall_score > 1:
            raise EvaluationValidationError(
                "overall_score must be between 0 and 1."
            )

        if not isinstance(self.recorded_at, datetime):
            raise EvaluationValidationError(
                "recorded_at must be datetime."
            )

        if self.notes is not None and not isinstance(self.notes, str):
            raise EvaluationValidationError(
                "notes must be string."
            )

    @staticmethod
    def _validate_non_empty_string(
        *,
        value: str,
        field_name: str,
    ) -> None:
        if not isinstance(value, str) or not value.strip():
            raise EvaluationValidationError(
                f"{field_name} must be non-empty string."
            )
