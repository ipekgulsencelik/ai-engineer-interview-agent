from __future__ import annotations

from typing import Any

from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)


class EvaluatorAlignmentReportSerializer:
    """
    Serializes EvaluatorAlignmentReport into primitive dictionaries.
    """

    @staticmethod
    def serialize(
        *,
        report: EvaluatorAlignmentReport,
    ) -> dict[str, Any]:
        return {
            "report_id": report.report_id,
            "evaluator_id": report.evaluator_id,
            "model_name": report.model_name,
            "pearson_correlation": {
                "metric_x": report.pearson_correlation.metric_x,
                "metric_y": report.pearson_correlation.metric_y,
                "correlation_coefficient": (
                    report.pearson_correlation.correlation_coefficient
                ),
                "p_value": report.pearson_correlation.p_value,
                "sample_count": report.pearson_correlation.sample_count,
                "method": report.pearson_correlation.method,
                "is_significant": (
                    report.pearson_correlation.is_significant
                ),
                "interpretation": (
                    report.pearson_correlation.interpretation
                ),
            },
            "agreement_result": {
                "metric_name": report.agreement_result.metric_name,
                "kappa_score": report.agreement_result.kappa_score,
                "agreement_ratio": (
                    report.agreement_result.agreement_ratio
                ),
                "sample_count": report.agreement_result.sample_count,
                "evaluator_count": (
                    report.agreement_result.evaluator_count
                ),
                "method": report.agreement_result.method,
                "is_reliable": report.agreement_result.is_reliable,
                "interpretation": (
                    report.agreement_result.interpretation
                ),
                "p_value": report.agreement_result.p_value,
                "notes": report.agreement_result.notes,
            },
            "regression_result": {
                "metric_name": report.regression_result.metric_name,
                "mae": report.regression_result.mae,
                "mse": report.regression_result.mse,
                "rmse": report.regression_result.rmse,
                "r2_score": report.regression_result.r2_score,
                "sample_count": report.regression_result.sample_count,
                "is_acceptable": report.regression_result.is_acceptable,
                "interpretation": (
                    report.regression_result.interpretation
                ),
                "notes": report.regression_result.notes,
            },
            "overall_alignment_score": report.overall_alignment_score,
            "is_strongly_aligned": report.is_strongly_aligned,
            "is_moderately_aligned": report.is_moderately_aligned,
            "is_weakly_aligned": report.is_weakly_aligned,
            "interpretation": report.interpretation,
            "notes": report.notes,
        }