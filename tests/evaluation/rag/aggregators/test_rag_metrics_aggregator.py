from __future__ import annotations

import pytest

from src.evaluation.rag.aggregators.rag_metrics_aggregator import RAGMetricsAggregator
from tests.evaluation.rag.factories import rag_result


def test_rag_metrics_aggregator_should_average_each_metric_across_results() -> None:
    snapshot = RAGMetricsAggregator().aggregate(
        results=(
            rag_result(result_id="r1", retrieval_precision=1.0, overall_score=1.0),
            rag_result(result_id="r2", retrieval_precision=0.0, overall_score=0.5),
        )
    )

    assert snapshot.average_retrieval_precision == 0.5
    assert snapshot.average_retrieval_recall == 1.0
    assert snapshot.average_overall_score == pytest.approx(0.75)
