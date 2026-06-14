from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError
from src.evaluation.reporting.validators.executive_summary_validator import ExecutiveSummaryValidator


def test_validate_accepts_valid_summary_payload(executive_summary) -> None:
    ExecutiveSummaryValidator.validate(
        summary_id=executive_summary.summary_id,
        title=executive_summary.title,
        overall_assessment=executive_summary.overall_assessment,
        key_findings=executive_summary.key_findings,
        strengths=executive_summary.strengths,
        weaknesses=executive_summary.weaknesses,
        recommendations=executive_summary.recommendations,
        overall_score=executive_summary.overall_score,
        pass_rate=executive_summary.pass_rate,
        total_runs=executive_summary.total_runs,
        average_score=executive_summary.average_score,
        best_score=executive_summary.best_score,
        risk_level=executive_summary.risk_level,
        trend_direction=executive_summary.trend_direction,
        confidence_level=executive_summary.confidence_level,
        recommendation=executive_summary.recommendation,
        generated_by=executive_summary.generated_by,
        notes=executive_summary.notes,
    )


def test_validate_rejects_blank_required_fields(executive_summary) -> None:
    with pytest.raises(EvaluationValidationError):
        ExecutiveSummaryValidator.validate(
            summary_id="",
            title=executive_summary.title,
            overall_assessment=executive_summary.overall_assessment,
            key_findings=executive_summary.key_findings,
            strengths=executive_summary.strengths,
            weaknesses=executive_summary.weaknesses,
            recommendations=executive_summary.recommendations,
            overall_score=executive_summary.overall_score,
            pass_rate=executive_summary.pass_rate,
            total_runs=executive_summary.total_runs,
            average_score=executive_summary.average_score,
            best_score=executive_summary.best_score,
            risk_level=executive_summary.risk_level,
            trend_direction=executive_summary.trend_direction,
            confidence_level=executive_summary.confidence_level,
            recommendation=executive_summary.recommendation,
            generated_by=executive_summary.generated_by,
            notes=executive_summary.notes,
        )
