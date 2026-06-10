from __future__ import annotations

import src.evaluation.metrics.builders as builders
from src.evaluation.metrics.builders.benchmark_aggregate_result_builder import (
    BenchmarkAggregateResultBuilder,
)
from src.evaluation.metrics.builders.benchmark_evaluation_report_builder import (
    BenchmarkEvaluationReportBuilder,
)
from src.evaluation.metrics.builders.category_metric_snapshot_builder import (
    CategoryMetricSnapshotBuilder,
)
from src.evaluation.metrics.builders.evaluator_alignment_report_builder import (
    EvaluatorAlignmentReportBuilder,
)
from src.evaluation.metrics.builders.trend_visualization_builder import (
    TrendVisualizationBuilder,
)


def test_builders_package_should_export_builder_classes() -> None:
    assert builders.__all__ == [
        "BenchmarkAggregateResultBuilder",
        "BenchmarkEvaluationReportBuilder",
        "CategoryMetricSnapshotBuilder",
        "EvaluatorAlignmentReportBuilder",
        "TrendVisualizationBuilder",
    ]
    assert builders.BenchmarkAggregateResultBuilder is BenchmarkAggregateResultBuilder
    assert builders.BenchmarkEvaluationReportBuilder is BenchmarkEvaluationReportBuilder
    assert builders.CategoryMetricSnapshotBuilder is CategoryMetricSnapshotBuilder
    assert builders.EvaluatorAlignmentReportBuilder is EvaluatorAlignmentReportBuilder
    assert builders.TrendVisualizationBuilder is TrendVisualizationBuilder
