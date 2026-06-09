from __future__ import annotations

from typing import Any

from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


class ExperimentResultSnapshotSerializer:
    """
    Serializes ExperimentResultSnapshot into JSON-safe dictionaries.
    """

    @classmethod
    def serialize(
        cls,
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
            "execution_time_seconds": (
                snapshot.execution_time_seconds
            ),
            "created_at": snapshot.created_at.isoformat(),
            "overall_score": snapshot.overall_score,
            "interpretation": snapshot.interpretation,
            "category_count": snapshot.category_count,
            "sample_count": snapshot.sample_count,
            "tags": list(snapshot.tags),
            "notes": snapshot.notes,
            "benchmark_report": cls._serialize_benchmark_report(
                report=snapshot.benchmark_report,
            ),
            "category_snapshots": [
                cls._serialize_category_snapshot(
                    snapshot=category_snapshot,
                )
                for category_snapshot in (
                    snapshot.benchmark_report.category_snapshots
                )
            ],
        }

    @classmethod
    def _serialize_benchmark_report(
        cls,
        *,
        report: BenchmarkEvaluationReport,
    ) -> dict[str, Any]:
        return {
            "benchmark_id": report.benchmark_id,
            "benchmark_name": report.benchmark_name,
            "benchmark_version": report.benchmark_version,
            "dataset_id": report.dataset_id,
            "dataset_version": report.dataset_version,
            "model_name": report.model_name,
            "evaluator_id": report.evaluator_id,
            "overall_score": report.overall_score,
            "interpretation": report.interpretation,
            "category_count": report.category_count,
            "sample_count": report.sample_count,
            "strongest_category": (
                report.strongest_category.category
                if report.strongest_category
                else None
            ),
            "weakest_category": (
                report.weakest_category.category
                if report.weakest_category
                else None
            ),
            "average_category_score": report.average_category_score,
            "notes": report.notes,
        }

    @classmethod
    def _serialize_category_snapshot(
        cls,
        *,
        snapshot: CategoryMetricSnapshot,
    ) -> dict[str, Any]:
        return {
            "category": snapshot.category,
            "sample_count": snapshot.sample_count,
            "average_human_score": snapshot.average_human_score,
            "average_llm_score": snapshot.average_llm_score,
            "score_delta": snapshot.score_delta,
            "absolute_score_delta": snapshot.absolute_score_delta,
            "pearson_correlation": snapshot.pearson_correlation,
            "kappa_score": snapshot.kappa_score,
            "agreement_ratio": snapshot.agreement_ratio,
            "mae": snapshot.mae,
            "mse": snapshot.mse,
            "rmse": snapshot.rmse,
            "r2_score": snapshot.r2_score,
            "overall_alignment_score": (
                snapshot.overall_alignment_score
            ),
            "interpretation": snapshot.interpretation,
            "has_positive_bias": snapshot.has_positive_bias,
            "has_negative_bias": snapshot.has_negative_bias,
            "is_neutral_bias": snapshot.is_neutral_bias,
            "notes": snapshot.notes,
        }