from __future__ import annotations

import math

from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError


class DatasetDriftSnapshotValidator:
    """DatasetDriftSnapshot validation service."""

    @staticmethod
    def validate(
        *,
        baseline_dataset_id: str,
        comparison_dataset_id: str,
        sample_count_delta: int,
        category_drift: dict[str, float],
        level_drift: dict[str, float],
        split_drift: dict[str, float],
        overall_drift_score: float,
        drift_detected: bool,
        notes: str | None,
    ) -> None:
        DatasetDriftSnapshotValidator._validate_non_empty_string(
            field_name="baseline_dataset_id",
            value=baseline_dataset_id,
        )
        DatasetDriftSnapshotValidator._validate_non_empty_string(
            field_name="comparison_dataset_id",
            value=comparison_dataset_id,
        )
        if isinstance(sample_count_delta, bool) or not isinstance(sample_count_delta, int):
            raise EvaluationValidationError("sample_count_delta must be int.")
        for field_name, drift_map in {
            "category_drift": category_drift,
            "level_drift": level_drift,
            "split_drift": split_drift,
        }.items():
            DatasetDriftSnapshotValidator._validate_drift_map(
                field_name=field_name,
                drift_map=drift_map,
            )
        DatasetDriftSnapshotValidator._validate_unit_score(
            field_name="overall_drift_score",
            value=overall_drift_score,
        )
        if not isinstance(drift_detected, bool):
            raise EvaluationValidationError("drift_detected must be bool.")
        if notes is not None and not isinstance(notes, str):
            raise EvaluationValidationError("notes must be str.")

    @staticmethod
    def _validate_non_empty_string(*, field_name: str, value: object) -> None:
        if not isinstance(value, str):
            raise EvaluationValidationError(f"{field_name} must be str.")
        if not value.strip():
            raise EvaluationValidationError(f"{field_name} cannot be empty.")

    @staticmethod
    def _validate_drift_map(*, field_name: str, drift_map: object) -> None:
        if not isinstance(drift_map, dict):
            raise EvaluationValidationError(f"{field_name} must be dict.")
        if not drift_map:
            raise EvaluationValidationError(f"{field_name} cannot be empty.")
        for key, value in drift_map.items():
            DatasetDriftSnapshotValidator._validate_non_empty_string(
                field_name=f"{field_name} keys",
                value=key,
            )
            DatasetDriftSnapshotValidator._validate_unit_score(
                field_name=f"{field_name} values",
                value=value,
            )

    @staticmethod
    def _validate_unit_score(*, field_name: str, value: object) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise EvaluationValidationError(f"{field_name} must be float.")
        if not math.isfinite(float(value)):
            raise EvaluationValidationError(f"{field_name} must be finite.")
        if float(value) < 0:
            raise EvaluationValidationError(
                f"{field_name} must be greater than or equal to 0."
            )
        if float(value) > 1:
            raise EvaluationValidationError(
                f"{field_name} must be less than or equal to 1."
            )
