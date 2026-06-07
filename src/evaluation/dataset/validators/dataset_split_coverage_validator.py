from __future__ import annotations

from src.evaluation.dataset.entities.dataset_split import (
    DatasetSplit,
)
from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class DatasetSplitCoverageValidator:
    """
    Validates split coverage against the source dataset.
    """

    @staticmethod
    def validate(
        *,
        dataset: EvaluationDataset,
        splits: tuple[DatasetSplit, ...],
    ) -> None:
        dataset_sample_ids = set(
            dataset.sample_ids,
        )

        split_sample_ids = [
            sample_id
            for split in splits
            for sample_id in split.sample_ids
        ]

        if len(split_sample_ids) != len(
            set(split_sample_ids),
        ):
            raise EvaluationValidationError(
                "split sample_ids must be unique across all splits."
            )

        unknown_sample_ids = set(
            split_sample_ids,
        ).difference(
            dataset_sample_ids,
        )

        if unknown_sample_ids:
            raise EvaluationValidationError(
                "split sample_ids contain unknown dataset samples: "
                f"{sorted(unknown_sample_ids)}"
            )

        missing_sample_ids = dataset_sample_ids.difference(
            split_sample_ids,
        )

        if missing_sample_ids:
            raise EvaluationValidationError(
                "splits do not cover all dataset samples: "
                f"{sorted(missing_sample_ids)}"
            )