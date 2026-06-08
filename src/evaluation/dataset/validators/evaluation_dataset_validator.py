from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.dataset.entities.dataset_metadata import (
    DatasetMetadata,
)
from src.evaluation.dataset.entities.dataset_version import (
    DatasetVersion,
)
from src.evaluation.dataset.schemas.evaluation_dataset_schema import (
    EVALUATION_DATASET_SCHEMA,
)
from src.evaluation.dataset.validators.evaluation_dataset_consistency_validator import (
    EvaluationDatasetConsistencyValidator,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class EvaluationDatasetValidator:
    """
    EvaluationDataset aggregate validation service.
    """

    @staticmethod
    def validate(
        *,
        dataset_id: str,
        dataset_name: str,
        dataset_version: DatasetVersion,
        description: str,
        metadata: DatasetMetadata,
        samples: tuple[EvaluationSample, ...],
        human_scores: tuple[HumanScore, ...],
        llm_scores: tuple[LLMScore, ...],
    ) -> None:
        SchemaValidator.validate(
            values={
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "description": description,
            },
            schema=EVALUATION_DATASET_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        EvaluationDatasetValidator._validate_dataset_version(
            dataset_version=dataset_version,
        )

        EvaluationDatasetValidator._validate_metadata(
            metadata=metadata,
        )

        EvaluationDatasetValidator._validate_samples(
            samples=samples,
        )

        EvaluationDatasetConsistencyValidator.validate(
            samples=samples,
            human_scores=human_scores,
            llm_scores=llm_scores,
        )

    @staticmethod
    def _validate_dataset_version(
        *,
        dataset_version: DatasetVersion,
    ) -> None:
        if not isinstance(
            dataset_version,
            DatasetVersion,
        ):
            raise EvaluationValidationError(
                "dataset_version must be a DatasetVersion."
            )

    @staticmethod
    def _validate_metadata(
        *,
        metadata: DatasetMetadata,
    ) -> None:
        if not isinstance(
            metadata,
            DatasetMetadata,
        ):
            raise EvaluationValidationError(
                "metadata must be a DatasetMetadata."
            )

    @staticmethod
    def _validate_samples(
        *,
        samples: tuple[EvaluationSample, ...],
    ) -> None:
        if not isinstance(
            samples,
            tuple,
        ):
            raise EvaluationValidationError(
                "samples must be a tuple."
            )

        if not samples:
            raise EvaluationValidationError(
                "dataset must contain at least one sample."
            )

        for index, sample in enumerate(samples):
            if not isinstance(
                sample,
                EvaluationSample,
            ):
                raise EvaluationValidationError(
                    f"samples[{index}] must be an EvaluationSample."
                )