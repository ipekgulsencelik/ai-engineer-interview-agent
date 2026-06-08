from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.dataset.enums.dataset_split_type import (
    DatasetSplitType,
)
from src.evaluation.dataset.schemas.dataset_split_schema import (
    DATASET_SPLIT_SCHEMA,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class DatasetSplitValidator:
    """
    DatasetSplit validation service.
    """

    @staticmethod
    def validate(
        *,
        split_type: DatasetSplitType,
        sample_ids: tuple[str, ...],
    ) -> None:
        DatasetSplitValidator._validate_split_type(
            split_type=split_type,
        )

        SchemaValidator.validate(
            values={
                "sample_ids": sample_ids,
            },
            schema=DATASET_SPLIT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        DatasetSplitValidator._validate_sample_ids(
            sample_ids=sample_ids,
        )

    @staticmethod
    def _validate_split_type(
        *,
        split_type: DatasetSplitType,
    ) -> None:
        if not isinstance(
            split_type,
            DatasetSplitType,
        ):
            raise EvaluationValidationError(
                "split_type must be a DatasetSplitType."
            )

    @staticmethod
    def _validate_sample_ids(
        *,
        sample_ids: tuple[str, ...],
    ) -> None:
        if not sample_ids:
            raise EvaluationValidationError(
                "sample_ids cannot be empty."
            )

        if len(sample_ids) != len(
            set(sample_ids),
        ):
            raise EvaluationValidationError(
                "sample_ids must be unique."
            )