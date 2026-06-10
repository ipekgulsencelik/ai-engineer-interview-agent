from __future__ import annotations

from collections.abc import Mapping

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.schemas.raw_human_annotation_schema import (
    HUMAN_ANNOTATION_REQUIRED_FIELDS,
)
from src.evaluation.dataset.types.raw_human_annotation_types import (
    RawHumanAnnotation,
)


class RawHumanAnnotationValidator:
    """
    Validates raw human annotation records before domain mapping.
    """

    @staticmethod
    def validate_record(
        *,
        record: object,
        index: int,
    ) -> RawHumanAnnotation:
        if not isinstance(
            record,
            Mapping,
        ):
            raise EvaluationDatasetLoadingError(
                f"Human annotation record at index {index} "
                "must be a JSON object."
            )

        RawHumanAnnotationValidator._validate_required_fields(
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
            HUMAN_ANNOTATION_REQUIRED_FIELDS
            .difference(
                record.keys(),
            )
        )

        if missing_fields:
            raise EvaluationDatasetLoadingError(
                f"Human annotation record at index {index} "
                f"is missing required fields: "
                f"{sorted(missing_fields)}"
            )