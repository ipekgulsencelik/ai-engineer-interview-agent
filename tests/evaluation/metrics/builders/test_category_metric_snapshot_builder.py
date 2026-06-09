from __future__ import annotations

import pytest

from src.evaluation.metrics.builders.category_metric_snapshot_builder import (
    CategoryMetricSnapshotBuilder,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)
from tests.evaluation.metrics.factories import (
    agreement_result,
    correlation_result,
    regression_result,
)


def test_category_metric_snapshot_builder_should_build_snapshot() -> None:
    snapshot = CategoryMetricSnapshotBuilder.build(
        category="RAG",
        human_scores=(3.0, 4.0, 5.0),
        llm_scores=(3.5, 4.5, 4.0),
        correlation_result=correlation_result(
            coefficient=0.90,
            sample_count=3,
        ),
        agreement_result=agreement_result(
            agreement_ratio=0.80,
            sample_count=3,
        ),
        regression_result=regression_result(
            r2_score=0.70,
            sample_count=3,
        ),
        notes="Category snapshot test.",
    )

    assert isinstance(snapshot, CategoryMetricSnapshot)
    assert snapshot.category == "RAG"
    assert snapshot.average_human_score == pytest.approx(4.0)
    assert snapshot.average_llm_score == pytest.approx(4.0)
    assert snapshot.overall_alignment_score == pytest.approx(0.80)
    assert snapshot.interpretation == "strong_alignment"
    assert snapshot.notes == "Category snapshot test."
