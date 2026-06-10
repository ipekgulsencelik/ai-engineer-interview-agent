from __future__ import annotations

from pathlib import Path

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.mappers.evaluation_sample_mapper import (
    EvaluationSampleMapper,
)
from src.evaluation.dataset.parsers.json_file_parser import (
    JsonFileParser,
)
from src.evaluation.dataset.validators.raw_evaluation_sample_validator import (
    RawEvaluationSampleValidator,
)
from src.evaluation.domain.entities.evaluation_sample import (
    EvaluationSample,
)


class EvaluationSampleLoader:
    """
    Loads EvaluationSample entities from JSON files.
    """

    def __init__(
        self,
        *,
        parser: JsonFileParser | None = None,
        raw_validator: RawEvaluationSampleValidator | None = None,
        mapper: EvaluationSampleMapper | None = None,
    ) -> None:
        self._parser = parser or JsonFileParser()
        self._raw_validator = (
            raw_validator
            or RawEvaluationSampleValidator()
        )
        self._mapper = mapper or EvaluationSampleMapper()

    def load(
        self,
        *,
        file_path: str | Path,
    ) -> tuple[EvaluationSample, ...]:
        path = Path(file_path)

        raw_data = self._parser.parse(
            file_path=path,
        )

        if not isinstance(
            raw_data,
            list,
        ):
            raise EvaluationDatasetLoadingError(
                "Evaluation sample file must contain a JSON array."
            )

        if not raw_data:
            raise EvaluationDatasetLoadingError(
                "Evaluation sample file cannot be empty."
            )

        samples: list[EvaluationSample] = []

        for index, record in enumerate(raw_data):
            validated_record = self._raw_validator.validate_record(
                record=record,
                index=index,
            )

            samples.append(
                self._mapper.map_record(
                    record=validated_record,
                    index=index,
                )
            )

        return tuple(samples)