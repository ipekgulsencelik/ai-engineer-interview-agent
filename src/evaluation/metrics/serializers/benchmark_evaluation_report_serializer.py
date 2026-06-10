from __future__ import annotations

from typing import Any

from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)


class BenchmarkEvaluationReportSerializer:
    """
    Serializes BenchmarkEvaluationReport into JSON-safe dictionaries.
    """

    @staticmethod
    def serialize(
        *,
        report: BenchmarkEvaluationReport,
    ) -> dict[str, Any]:
        return {
            "benchmark_id": report.benchmark_id,
            "benchmark_name": report.benchmark_name,
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
                report.weakest_category.category if report.weakest_category else None
            ),
            "average_category_score": report.average_category_score,
            "notes": report.notes,
        }
