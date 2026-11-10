"""Adapter for evaluating serialized EvaluationDataset sample records."""

from __future__ import annotations

from typing import Any

from src.evaluation.dataset.entities.evaluation_dataset import EvaluationDataset
from src.evaluation.dataset.quality.engine import DatasetQualityEngine
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.serializers.evaluation_dataset_serializer import (
    EvaluationDatasetSerializer,
)


class EvaluationDatasetQualityAdapter:
    """Use the existing aggregate serializer, not a parallel field mapper."""

    def __init__(self, *, engine: DatasetQualityEngine) -> None:
        self._engine = engine

    def evaluate(self, *, dataset: EvaluationDataset) -> QualityReport:
        payload = EvaluationDatasetSerializer.serialize(dataset=dataset)
        records: list[dict[str, Any]] = payload["samples"]
        return self._engine.evaluate(
            dataset_id=dataset.dataset_id,
            dataset_version=dataset.dataset_version.version,
            records=records,
        )
