from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from src.domain.enums.level import Level
from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.types.raw_evaluation_sample_types import (
    RawEvaluationSample,
)
from src.evaluation.domain.entities.evaluation_sample import (
    EvaluationSample,
)


class EvaluationSampleMapper:
    """
    Maps validated raw JSON records into EvaluationSample entities.
    """

    @staticmethod
    def map_record(
        *,
        record: RawEvaluationSample,
        index: int,
    ) -> EvaluationSample:
        try:
            return EvaluationSample(
                sample_id=EvaluationSampleMapper._get_string(
                    record=record,
                    field_name="sample_id",
                    index=index,
                ),
                question_id=EvaluationSampleMapper._get_string(
                    record=record,
                    field_name="question_id",
                    index=index,
                ),
                question=EvaluationSampleMapper._get_string(
                    record=record,
                    field_name="question",
                    index=index,
                ),
                candidate_answer=EvaluationSampleMapper._get_string(
                    record=record,
                    field_name="candidate_answer",
                    index=index,
                ),
                expected_answer=EvaluationSampleMapper._get_string(
                    record=record,
                    field_name="expected_answer",
                    index=index,
                ),
                category=EvaluationSampleMapper._get_string(
                    record=record,
                    field_name="category",
                    index=index,
                ),
                level=EvaluationSampleMapper._get_level(
                    record=record,
                    index=index,
                ),
                retrieved_contexts=EvaluationSampleMapper._get_contexts(
                    record=record,
                    index=index,
                ),
                metadata=EvaluationSampleMapper._get_metadata(
                    record=record,
                    index=index,
                ),
            )
        except EvaluationDatasetLoadingError:
            raise
        except ValueError as exc:
            raise EvaluationDatasetLoadingError(
                f"Invalid EvaluationSample value at index {index}."
            ) from exc
        except TypeError as exc:
            raise EvaluationDatasetLoadingError(
                f"Invalid EvaluationSample record type at index {index}."
            ) from exc

    @staticmethod
    def _get_string(
        *,
        record: Mapping[str, object],
        field_name: str,
        index: int,
    ) -> str:
        value = record[field_name]

        if not isinstance(value, str):
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index {index} "
                f"field '{field_name}' must be a string."
            )

        return value

    @staticmethod
    def _get_level(
        *,
        record: Mapping[str, object],
        index: int,
    ) -> Level:
        raw_level = record["level"]

        if not isinstance(raw_level, str):
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index {index} "
                "field 'level' must be a string."
            )

        normalized_level = raw_level.strip().upper()

        try:
            return Level(normalized_level)
        except ValueError as exc:
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index {index} "
                f"has invalid level: {raw_level}"
            ) from exc

    @staticmethod
    def _get_contexts(
        *,
        record: Mapping[str, object],
        index: int,
    ) -> tuple[str, ...]:
        raw_contexts = record.get(
            "retrieved_contexts",
            (),
        )

        if raw_contexts is None:
            return ()

        if not isinstance(
            raw_contexts,
            (list, tuple),
        ):
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index {index} "
                "field 'retrieved_contexts' must be a list or tuple."
            )

        contexts: list[str] = []

        for context_index, context in enumerate(raw_contexts):
            if not isinstance(context, str):
                raise EvaluationDatasetLoadingError(
                    f"Evaluation sample record at index {index} "
                    f"retrieved_contexts[{context_index}] "
                    "must be a string."
                )

            contexts.append(context)

        return tuple(contexts)

    @staticmethod
    def _get_metadata(
        *,
        record: Mapping[str, object],
        index: int,
    ) -> dict[str, object]:
        raw_metadata = record.get(
            "metadata",
            {},
        )

        if raw_metadata is None:
            return {}

        if not isinstance(raw_metadata, dict):
            raise EvaluationDatasetLoadingError(
                f"Evaluation sample record at index {index} "
                "field 'metadata' must be an object."
            )

        return cast(
            dict[str, object],
            raw_metadata,
        )