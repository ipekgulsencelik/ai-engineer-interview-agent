from __future__ import annotations

import pytest

from src.evaluation.metrics.serializers.category_metric_snapshot_serializer import (
    CategoryMetricSnapshotSerializer,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _category_snapshot,
)


def test_category_metric_snapshot_serializer_should_serialize_metric_fields() -> None:
    snapshot = _category_snapshot(category="RAG", score=0.90)

    payload = CategoryMetricSnapshotSerializer.serialize(snapshot=snapshot)

    assert payload["category"] == "RAG"
    assert payload["sample_count"] == 4
    assert payload["average_human_score"] == pytest.approx(8.0)
    assert payload["average_llm_score"] == pytest.approx(8.2)
    assert payload["score_delta"] == pytest.approx(0.2)
    assert payload["absolute_score_delta"] == pytest.approx(0.2)
    assert payload["pearson_correlation"] == pytest.approx(0.90)
    assert payload["kappa_score"] == pytest.approx(0.80)
    assert payload["agreement_ratio"] == pytest.approx(0.80)
    assert payload["mae"] == pytest.approx(0.10)
    assert payload["mse"] == pytest.approx(0.01)
    assert payload["rmse"] == pytest.approx(0.10)
    assert payload["r2_score"] == pytest.approx(0.70)
    assert payload["overall_alignment_score"] == pytest.approx(0.90)
    assert payload["interpretation"] == "category_alignment"
    assert payload["has_positive_bias"] is True
    assert payload["has_negative_bias"] is False
    assert payload["is_neutral_bias"] is False
    assert payload["notes"] is None
