from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.reporting.enums.summary_trend_direction import (
    SummaryTrendDirection,
)
from src.evaluation.reporting.validators.executive_summary_validator import (
    ExecutiveSummaryValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExecutiveSummary:
    """
    Immutable executive summary.

    High-level business and technical summary
    of an evaluation, benchmark, experiment,
    model release, or dataset assessment.
    """

    summary_id: str

    title: str

    overall_assessment: str

    key_findings: tuple[
        str,
        ...,
    ]

    strengths: tuple[
        str,
        ...,
    ]

    weaknesses: tuple[
        str,
        ...,
    ]

    recommendations: tuple[
        str,
        ...,
    ]

    overall_score: float | None = None

    pass_rate: float | None = None

    total_runs: int | None = None

    average_score: float | None = None

    best_score: float | None = None

    risk_level: str | None = None

    trend_direction: SummaryTrendDirection | None = None

    confidence_level: float | None = None

    recommendation: str | None = None

    generated_by: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExecutiveSummaryValidator.validate(
            summary_id=self.summary_id,
            title=self.title,
            overall_assessment=self.overall_assessment,
            key_findings=self.key_findings,
            strengths=self.strengths,
            weaknesses=self.weaknesses,
            recommendations=self.recommendations,
            overall_score=self.overall_score,
            pass_rate=self.pass_rate,
            total_runs=self.total_runs,
            average_score=self.average_score,
            best_score=self.best_score,
            risk_level=self.risk_level,
            trend_direction=self.trend_direction,
            confidence_level=self.confidence_level,
            recommendation=self.recommendation,
            generated_by=self.generated_by,
            notes=self.notes,
        )

    @property
    def has_findings(
        self,
    ) -> bool:
        return bool(
            self.key_findings,
        )

    @property
    def has_strengths(
        self,
    ) -> bool:
        return bool(
            self.strengths,
        )

    @property
    def has_weaknesses(
        self,
    ) -> bool:
        return bool(
            self.weaknesses,
        )

    @property
    def has_recommendations(
        self,
    ) -> bool:
        return bool(
            self.recommendations,
        )

    @property
    def has_score(
        self,
    ) -> bool:
        return (
            self.overall_score
            is not None
        )

    @property
    def has_pass_rate(
        self,
    ) -> bool:
        return (
            self.pass_rate
            is not None
        )

    @property
    def has_run_metrics(
        self,
    ) -> bool:
        return (
            self.total_runs
            is not None
        )

    @property
    def has_average_score(
        self,
    ) -> bool:
        return (
            self.average_score
            is not None
        )

    @property
    def has_best_score(
        self,
    ) -> bool:
        return (
            self.best_score
            is not None
        )

    @property
    def has_risk_level(
        self,
    ) -> bool:
        return (
            self.risk_level
            is not None
        )

    @property
    def has_confidence_level(
        self,
    ) -> bool:
        return (
            self.confidence_level
            is not None
        )

    @property
    def has_trend_direction(
        self,
    ) -> bool:
        return (
            self.trend_direction
            is not None
        )

    @property
    def has_recommendation(
        self,
    ) -> bool:
        return (
            self.recommendation
            is not None
        )

    @property
    def is_improving(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.IMPROVING
        )

    @property
    def is_declining(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.DECLINING
        )

    @property
    def is_stable(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.STABLE
        )

    @property
    def is_volatile(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.VOLATILE
        )