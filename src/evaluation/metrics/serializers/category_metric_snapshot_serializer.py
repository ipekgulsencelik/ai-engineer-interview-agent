from __future__ import annotations

from typing import Any

from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


class CategoryMetricSnapshotSerializer:
    """
    Serializes CategoryMetricSnapshot into JSON-safe dictionaries.
    """

    @staticmethod
    def serialize(
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
            "overall_alignment_score": snapshot.overall_alignment_score,
            "interpretation": snapshot.interpretation,
            "has_positive_bias": snapshot.has_positive_bias,
            "has_negative_bias": snapshot.has_negative_bias,
            "is_neutral_bias": snapshot.is_neutral_bias,
            "notes": snapshot.notes,
        }
