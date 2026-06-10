from __future__ import annotations

import random

from src.evaluation.dataset.constants.dataset_splits import (
    DEFAULT_SPLIT_SEED,
    DEFAULT_TEST_RATIO,
    DEFAULT_TRAIN_RATIO,
    DEFAULT_VALIDATION_RATIO,
    MIN_SPLITTABLE_SAMPLE_COUNT,
)
from src.evaluation.dataset.value_objects.dataset_split import (
    DatasetSplit,
)
from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)
from src.evaluation.dataset.enums.dataset_split_type import (
    DatasetSplitType,
)
from src.evaluation.dataset.validators.dataset_split_ratio_validator import (
    DatasetSplitRatioValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class DatasetSplitter:
    """
    Deterministic train/validation/test dataset splitter.
    """

    @staticmethod
    def split(
        *,
        dataset: EvaluationDataset,
        train_ratio: float = DEFAULT_TRAIN_RATIO,
        validation_ratio: float = DEFAULT_VALIDATION_RATIO,
        test_ratio: float = DEFAULT_TEST_RATIO,
        seed: int = DEFAULT_SPLIT_SEED,
    ) -> tuple[
        DatasetSplit,
        DatasetSplit,
        DatasetSplit,
    ]:
        DatasetSplitRatioValidator.validate(
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
        )

        DatasetSplitter._validate_dataset_size(
            dataset=dataset,
        )

        shuffled_sample_ids = list(
            dataset.sample_ids,
        )

        random.Random(
            seed,
        ).shuffle(
            shuffled_sample_ids,
        )

        total_count = len(
            shuffled_sample_ids,
        )

        train_count = int(
            total_count * train_ratio,
        )

        validation_count = int(
            total_count * validation_ratio,
        )

        train_ids = tuple(
            shuffled_sample_ids[
                :train_count
            ],
        )

        validation_ids = tuple(
            shuffled_sample_ids[
                train_count:
                train_count
                + validation_count
            ],
        )

        test_ids = tuple(
            shuffled_sample_ids[
                train_count
                + validation_count:
            ],
        )

        return (
            DatasetSplit(
                split_type=DatasetSplitType.TRAIN,
                sample_ids=train_ids,
            ),
            DatasetSplit(
                split_type=DatasetSplitType.VALIDATION,
                sample_ids=validation_ids,
            ),
            DatasetSplit(
                split_type=DatasetSplitType.TEST,
                sample_ids=test_ids,
            ),
        )

    @staticmethod
    def _validate_dataset_size(
        *,
        dataset: EvaluationDataset,
    ) -> None:
        if (
            dataset.sample_count
            < MIN_SPLITTABLE_SAMPLE_COUNT
        ):
            raise EvaluationValidationError(
                "dataset must contain at least "
                f"{MIN_SPLITTABLE_SAMPLE_COUNT} "
                "samples to create train, "
                "validation, and test splits."
            )