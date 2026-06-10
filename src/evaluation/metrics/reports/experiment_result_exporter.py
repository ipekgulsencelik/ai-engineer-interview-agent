from __future__ import annotations

import json
from pathlib import Path

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.serializers.experiment_result_snapshot_serializer import (
    ExperimentResultSnapshotSerializer,
)


class ExperimentResultExporter:
    """
    Exports experiment result snapshots as deterministic JSON artifacts.
    """

    def __init__(
        self,
        *,
        serializer: ExperimentResultSnapshotSerializer | None = None,
    ) -> None:
        self._serializer = (
            serializer
            or ExperimentResultSnapshotSerializer()
        )

    def export(
        self,
        *,
        snapshot: ExperimentResultSnapshot,
        output_path: str | Path,
    ) -> Path:
        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = self._serializer.serialize(
            snapshot=snapshot,
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