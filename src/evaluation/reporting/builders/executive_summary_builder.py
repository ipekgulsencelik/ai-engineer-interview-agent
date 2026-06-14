from __future__ import annotations

from uuid import uuid4

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.enums.summary_trend_direction import (
    SummaryTrendDirection,
)
from src.evaluation.reporting.interpreters.executive_summary_assessment_interpreter import (
    ExecutiveSummaryAssessmentInterpreter,
)
from src.evaluation.reporting.recommenders.executive_summary_recommender import (
    ExecutiveSummaryRecommender,
)


class ExecutiveSummaryBuilder:
    """
    Builder for executive summary entities.
    """

    def __init__(
        self,
        *,
        assessment_interpreter: (
            ExecutiveSummaryAssessmentInterpreter | None
        ) = None,
        recommender: ExecutiveSummaryRecommender | None = None,
    ) -> None:
        self._assessment_interpreter = (
            assessment_interpreter
            or ExecutiveSummaryAssessmentInterpreter()
        )
        self._recommender = (
            recommender
            or ExecutiveSummaryRecommender()
        )

    def build(
        self,
        *,
        title: str,
        overall_assessment: str,
        key_findings: tuple[
            str,
            ...,
        ] = (),
        strengths: tuple[
            str,
            ...,
        ] = (),
        weaknesses: tuple[
            str,
            ...,
        ] = (),
        recommendations: tuple[
            str,
            ...,
        ] = (),
        overall_score: float | None = None,
        pass_rate: float | None = None,
        total_runs: int | None = None,
        average_score: float | None = None,
        best_score: float | None = None,
        risk_level: str | None = None,
        trend_direction: SummaryTrendDirection | None = None,
        confidence_level: float | None = None,
        recommendation: str | None = None,
        generated_by: str | None = None,
        notes: str | None = None,
    ) -> ExecutiveSummary:
        return ExecutiveSummary(
            summary_id=str(
                uuid4(),
            ),
            title=title,
            overall_assessment=overall_assessment,
            key_findings=key_findings,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            overall_score=overall_score,
            pass_rate=pass_rate,
            total_runs=total_runs,
            average_score=average_score,
            best_score=best_score,
            risk_level=risk_level,
            trend_direction=trend_direction,
            confidence_level=confidence_level,
            recommendation=recommendation,
            generated_by=generated_by,
            notes=notes,
        )

    def build_from_metrics(
        self,
        *,
        title: str,
        overall_score: float,
        pass_rate: float,
        total_runs: int,
        average_score: float,
        best_score: float,
        trend_direction: SummaryTrendDirection,
        key_findings: tuple[
            str,
            ...,
        ] = (),
        strengths: tuple[
            str,
            ...,
        ] = (),
        weaknesses: tuple[
            str,
            ...,
        ] = (),
        recommendations: tuple[
            str,
            ...,
        ] = (),
        risk_level: str | None = None,
        confidence_level: float | None = None,
        recommendation: str | None = None,
        generated_by: str | None = None,
        notes: str | None = None,
    ) -> ExecutiveSummary:
        return self.build(
            title=title,
            overall_assessment=(
                self._assessment_interpreter.interpret(
                    overall_score=overall_score,
                )
            ),
            key_findings=key_findings,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            overall_score=overall_score,
            pass_rate=pass_rate,
            total_runs=total_runs,
            average_score=average_score,
            best_score=best_score,
            risk_level=risk_level,
            trend_direction=trend_direction,
            confidence_level=confidence_level,
            recommendation=(
                recommendation
                or self._recommender.recommend(
                    trend_direction=trend_direction,
                    overall_score=overall_score,
                    pass_rate=pass_rate,
                )
            ),
            generated_by=generated_by,
            notes=notes,
        )