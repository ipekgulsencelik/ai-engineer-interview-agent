from __future__ import annotations

import json
from pathlib import Path

from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)
from src.evaluation.dataset.serializers.evaluation_dataset_serializer import (
    EvaluationDatasetSerializer,
)


class EvaluationDatasetExporter:
    """
    Exports EvaluationDataset aggregates into deterministic JSON artifacts.
    """

    def __init__(
        self,
        *,
        serializer: EvaluationDatasetSerializer | None = None,
    ) -> None:
        self._serializer = serializer or EvaluationDatasetSerializer()

    def export(
        self,
        *,
        dataset: EvaluationDataset,
        output_path: str | Path,
    ) -> Path:
        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = self._serializer.serialize(
            dataset=dataset,
        )

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        return path