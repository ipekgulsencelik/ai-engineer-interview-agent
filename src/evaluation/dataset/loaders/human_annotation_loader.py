from __future__ import annotations

from pathlib import Path

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.mappers.human_annotation_mapper import (
    HumanAnnotationMapper,
)
from src.evaluation.dataset.parsers.json_file_parser import (
    JsonFileParser,
)
from src.evaluation.dataset.validators.raw_human_annotation_validator import (
    RawHumanAnnotationValidator,
)
from src.evaluation.domain.entities.human_score import (
    HumanScore,
)


class HumanAnnotationLoader:
    """
    Loads HumanScore entities from human annotation JSON files.
    """

    def __init__(
        self,
        *,
        parser: JsonFileParser | None = None,
        raw_validator: RawHumanAnnotationValidator | None = None,
        mapper: HumanAnnotationMapper | None = None,
    ) -> None:
        self._parser = parser or JsonFileParser()
        self._raw_validator = (
            raw_validator
            or RawHumanAnnotationValidator()
        )
        self._mapper = mapper or HumanAnnotationMapper()

    def load(
        self,
        *,
        file_path: str | Path,
    ) -> tuple[HumanScore, ...]:
        path = Path(file_path)

        raw_data = self._parser.parse(
            file_path=path,
        )

        if not isinstance(
            raw_data,
            list,
        ):
            raise EvaluationDatasetLoadingError(
                "Human annotation file must contain a JSON array."
            )

        if not raw_data:
            raise EvaluationDatasetLoadingError(
                "Human annotation file cannot be empty."
            )

        human_scores: list[HumanScore] = []

        for index, record in enumerate(raw_data):
            validated_record = self._raw_validator.validate_record(
                record=record,
                index=index,
            )

            human_scores.append(
                self._mapper.map_record(
                    record=validated_record,
                    index=index,
                )
            )

        return tuple(human_scores)