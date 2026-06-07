from __future__ import annotations

from collections.abc import Mapping

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.types.raw_human_annotation_types import (
    RawHumanAnnotation,
)
from src.evaluation.domain.entities.human_score import (
    HumanScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class HumanAnnotationMapper:
    """
    Maps validated raw human annotation records into HumanScore entities.
    """

    @staticmethod
    def map_record(
        *,
        record: RawHumanAnnotation,
        index: int,
    ) -> HumanScore:
        try:
            return HumanScore(
                sample_id=HumanAnnotationMapper._get_string(
                    record=record,
                    field_name="sample_id",
                    index=index,
                ),
                evaluator_id=HumanAnnotationMapper._get_string(
                    record=record,
                    field_name="evaluator_id",
                    index=index,
                ),
                overall_score=HumanAnnotationMapper._get_number(
                    record=record,
                    field_name="overall_score",
                    index=index,
                ),
                technical_score=HumanAnnotationMapper._get_number(
                    record=record,
                    field_name="technical_score",
                    index=index,
                ),
                communication_score=HumanAnnotationMapper._get_number(
                    record=record,
                    field_name="communication_score",
                    index=index,
                ),
                feedback=HumanAnnotationMapper._get_string(
                    record=record,
                    field_name="feedback",
                    index=index,
                ),
            )
        except EvaluationDatasetLoadingError:
            raise
        except EvaluationValidationError as exc:
            raise EvaluationDatasetLoadingError(
                f"Invalid HumanScore domain value at index {index}."
            ) from exc
        except ValueError as exc:
            raise EvaluationDatasetLoadingError(
                f"Invalid HumanScore value at index {index}."
            ) from exc
        except TypeError as exc:
            raise EvaluationDatasetLoadingError(
                f"Invalid HumanScore record type at index {index}."
            ) from exc

    @staticmethod
    def _get_string(
        *,
        record: Mapping[str, object],
        field_name: str,
        index: int,
    ) -> str:
        value = record[field_name]

        if not isinstance(
            value,
            str,
        ):
            raise EvaluationDatasetLoadingError(
                f"Human annotation record at index {index} "
                f"field '{field_name}' must be a string."
            )

        return value

    @staticmethod
    def _get_number(
        *,
        record: Mapping[str, object],
        field_name: str,
        index: int,
    ) -> float:
        value = record[field_name]

        if (
            isinstance(value, bool)
            or not isinstance(
                value,
                (int, float),
            )
        ):
            raise EvaluationDatasetLoadingError(
                f"Human annotation record at index {index} "
                f"field '{field_name}' must be numeric."
            )

        return float(value)