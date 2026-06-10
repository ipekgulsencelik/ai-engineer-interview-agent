from __future__ import annotations

from typing import Any

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.serializers.benchmark_evaluation_report_serializer import (
    BenchmarkEvaluationReportSerializer,
)
from src.evaluation.metrics.serializers.category_metric_snapshot_serializer import (
    CategoryMetricSnapshotSerializer,
)


class ExperimentResultSnapshotSerializer:
    """
    Serializes ExperimentResultSnapshot into JSON-safe dictionaries.
    """

    @staticmethod
    def serialize(
        *,
        snapshot: ExperimentResultSnapshot,
    ) -> dict[str, Any]:
        return {
            "experiment_id": snapshot.experiment_id,
            "benchmark_id": snapshot.benchmark_id,
            "benchmark_version": snapshot.benchmark_version,
            "benchmark_name": snapshot.benchmark_name,
            "dataset_id": snapshot.dataset_id,
            "dataset_version": snapshot.dataset_version,
            "dataset_hash": snapshot.dataset_hash,
            "model_name": snapshot.model_name,
            "metrics_version": snapshot.metrics_version,
            "execution_time_seconds": snapshot.execution_time_seconds,
            "created_at": snapshot.created_at.isoformat(),
            "overall_score": snapshot.overall_score,
            "interpretation": snapshot.interpretation,
            "category_count": snapshot.category_count,
            "sample_count": snapshot.sample_count,
            "tags": list(snapshot.tags),
            "notes": snapshot.notes,
            "benchmark_report": BenchmarkEvaluationReportSerializer.serialize(
                report=snapshot.benchmark_report,
            ),
            "category_snapshots": [
                CategoryMetricSnapshotSerializer.serialize(
                    snapshot=category_snapshot,
                )
                for category_snapshot in snapshot.benchmark_report.category_snapshots
            ],
        }
