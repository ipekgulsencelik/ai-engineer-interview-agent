from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


def _correlation_result() -> CorrelationResult:
    return CorrelationResult(
        metric_x="human_score",
        metric_y="llm_score",
        correlation_coefficient=0.90,
        p_value=0.01,
        sample_count=4,
        method="pearson",
        is_significant=True,
        interpretation="very_strong",
    )


def _agreement_result() -> AgreementResult:
    return AgreementResult(
        metric_name="human_llm_agreement",
        kappa_score=0.80,
        agreement_ratio=0.80,
        sample_count=4,
        evaluator_count=2,
        method="cohen_kappa",
        is_reliable=True,
        interpretation="strong",
    )


def _regression_result() -> RegressionMetricResult:
    return RegressionMetricResult(
        metric_name="human_llm_regression",
        mae=0.10,
        mse=0.01,
        rmse=0.10,
        r2_score=0.70,
        sample_count=4,
        is_acceptable=True,
        interpretation="moderate",
    )


def _alignment_report() -> EvaluatorAlignmentReport:
    return EvaluatorAlignmentReport(
        report_id="alignment-report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        pearson_correlation=_correlation_result(),
        agreement_result=_agreement_result(),
        regression_result=_regression_result(),
        overall_alignment_score=0.80,
        interpretation="strong_alignment",
    )


def _category_snapshot(
    *,
    category: str,
    score: float,
) -> CategoryMetricSnapshot:
    return CategoryMetricSnapshot(
        category=category,
        average_human_score=8.0,
        average_llm_score=8.2,
        correlation_result=_correlation_result(),
        agreement_result=_agreement_result(),
        regression_result=_regression_result(),
        overall_alignment_score=score,
        interpretation="category_alignment",
    )


def test_benchmark_evaluation_report_should_create_successfully() -> None:
    report = BenchmarkEvaluationReport(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(
                category="RAG",
                score=0.90,
            ),
            _category_snapshot(
                category="Agents",
                score=0.70,
            ),
        ),
        overall_score=0.80,
        interpretation="strong_benchmark",
        notes="Valid benchmark report.",
    )

    assert report.benchmark_id == "benchmark-1"
    assert report.benchmark_name == "AI Engineer Benchmark"
    assert report.benchmark_version == "1.0.0"
    assert report.dataset_id == "dataset-1"
    assert report.dataset_version == "1.0.0"
    assert report.category_count == 2
    assert report.sample_count == 8
    assert report.strongest_category.category == "RAG"
    assert report.weakest_category.category == "Agents"
    assert report.average_category_score == pytest.approx(0.80)


@pytest.mark.parametrize(
    "field_name",
    [
        "benchmark_id",
        "benchmark_name",
        "benchmark_version",
        "dataset_id",
        "dataset_version",
        "model_name",
        "evaluator_id",
        "interpretation",
    ],
)
def test_benchmark_evaluation_report_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = {
        "benchmark_id": "benchmark-1",
        "benchmark_name": "AI Engineer Benchmark",
        "benchmark_version": "1.0.0",
        "dataset_id": "dataset-1",
        "dataset_version": "1.0.0",
        "model_name": "gpt-5",
        "evaluator_id": "evaluator-1",
        "alignment_report": _alignment_report(),
        "category_snapshots": (
            _category_snapshot(
                category="RAG",
                score=0.90,
            ),
        ),
        "overall_score": 0.80,
        "interpretation": "strong_benchmark",
        "notes": None,
    }
    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
    ):
        BenchmarkEvaluationReport(**kwargs)


def test_benchmark_evaluation_report_should_raise_for_invalid_overall_score() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        BenchmarkEvaluationReport(
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            benchmark_version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            model_name="gpt-5",
            evaluator_id="evaluator-1",
            alignment_report=_alignment_report(),
            category_snapshots=(),
            overall_score=1.5,
            interpretation="invalid",
        )


def test_benchmark_evaluation_report_should_be_immutable() -> None:
    report = BenchmarkEvaluationReport(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(),
        overall_score=0.80,
        interpretation="strong_benchmark",
    )

    with pytest.raises(
        AttributeError,
    ):
        report.benchmark_id = "changed"  # type: ignore[misc]