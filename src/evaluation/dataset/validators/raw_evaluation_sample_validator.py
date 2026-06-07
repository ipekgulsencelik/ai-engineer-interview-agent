from __future__ import annotations

from collections.abc import Mapping

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.schemas.raw_evaluation_sample_schema import (
    REQUIRED_EVALUATION_SAMPLE_FIELDS,
)
from src.evaluation.dataset.types.raw_evaluation_sample_types import (
    RawEvaluationSample,
)


class RawEvaluationSampleValidator:
    """
    Validates raw EvaluationSample records before domain mapping.
    """

    @staticmethod
    def validate_record(
        *,
        record: object,
        index: int,
    ) -> RawEvaluationSample:
        if not isinstance(
            record,
            Mapping,
        ):
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index "
                f"{index} must be a JSON object."
            )

        RawEvaluationSampleValidator._validate_required_fields(
            record=record,
            index=index,
        )

        return record

    @staticmethod
    def _validate_required_fields(
        *,
        record: Mapping[str, object],
        index: int,
    ) -> None:
        missing_fields = (
            REQUIRED_EVALUATION_SAMPLE_FIELDS
            .difference(
                record.keys(),
            )
        )

        if missing_fields:
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index "
                f"{index} is missing required fields: "
                f"{sorted(missing_fields)}"
            )