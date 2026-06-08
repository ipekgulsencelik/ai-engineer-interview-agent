from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError


class DatasetDistributionSnapshotValidator:
    """DatasetDistributionSnapshot validation service."""

    @staticmethod
    def validate(
        *,
        dataset_id: str,
        sample_count: int,
        category_distribution: dict[str, int],
        level_distribution: dict[str, int],
        split_distribution: dict[str, int],
    ) -> None:
        if not isinstance(dataset_id, str):
            raise EvaluationValidationError("dataset_id must be str.")
        if not dataset_id.strip():
            raise EvaluationValidationError("dataset_id cannot be empty.")
        if isinstance(sample_count, bool) or not isinstance(sample_count, int):
            raise EvaluationValidationError("sample_count must be int.")
        if sample_count < 0:
            raise EvaluationValidationError(
                "sample_count must be greater than or equal to 0."
            )

        for field_name, distribution in {
            "category_distribution": category_distribution,
            "level_distribution": level_distribution,
            "split_distribution": split_distribution,
        }.items():
            DatasetDistributionSnapshotValidator._validate_distribution(
                field_name=field_name,
                distribution=distribution,
            )

    @staticmethod
    def _validate_distribution(
        *,
        field_name: str,
        distribution: object,
    ) -> None:
        if not isinstance(distribution, dict):
            raise EvaluationValidationError(f"{field_name} must be dict.")
        if not distribution:
            raise EvaluationValidationError(f"{field_name} cannot be empty.")
        for key, value in distribution.items():
            if not isinstance(key, str):
                raise EvaluationValidationError(f"{field_name} keys must be str.")
            if not key.strip():
                raise EvaluationValidationError(f"{field_name} keys cannot be empty.")
            if isinstance(value, bool) or not isinstance(value, int):
                raise EvaluationValidationError(f"{field_name} values must be int.")
            if value < 0:
                raise EvaluationValidationError(
                    f"{field_name} values must be greater than or equal to 0."
                )
