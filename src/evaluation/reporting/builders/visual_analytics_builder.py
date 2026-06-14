from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.calculators.visual_average_score_calculator import (
    VisualAverageScoreCalculator,
)
from src.evaluation.reporting.detectors.visual_trend_direction_detector import (
    VisualTrendDirectionDetector,
)
from src.evaluation.reporting.entities.visual_analytics_snapshot import (
    VisualAnalyticsSnapshot,
)
from src.evaluation.reporting.enums.summary_trend_direction import (
    SummaryTrendDirection,
)
from src.evaluation.reporting.mappers.experiment_trend_visual_mapper import (
    ExperimentTrendVisualMapper,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class VisualAnalyticsBuilder:
    """
    Builder for chart-ready visual analytics snapshots.
    """

    def __init__(
        self,
        *,
        average_score_calculator: (
            VisualAverageScoreCalculator | None
        ) = None,
        trend_direction_detector: (
            VisualTrendDirectionDetector | None
        ) = None,
        trend_visual_mapper: (
            ExperimentTrendVisualMapper | None
        ) = None,
    ) -> None:
        self._average_score_calculator = (
            average_score_calculator
            or VisualAverageScoreCalculator()
        )
        self._trend_direction_detector = (
            trend_direction_detector
            or VisualTrendDirectionDetector()
        )
        self._trend_visual_mapper = (
            trend_visual_mapper
            or ExperimentTrendVisualMapper()
        )

    def build(
        self,
        *,
        title: str,
        chart_type: str,
        labels: tuple[
            str,
            ...,
        ],
        scores: tuple[
            float,
            ...,
        ],
        average_score: float | None = None,
        trend_direction: SummaryTrendDirection | None = None,
        x_axis_label: str | None = None,
        y_axis_label: str | None = None,
        series_name: str | None = None,
        experiment_id: str | None = None,
        run_id: str | None = None,
        benchmark_id: str | None = None,
        model_name: str | None = None,
        description: str | None = None,
        metadata: dict[
            str,
            str,
        ] | None = None,
        created_at: datetime | None = None,
    ) -> VisualAnalyticsSnapshot:
        return VisualAnalyticsSnapshot(
            snapshot_id=str(
                uuid4(),
            ),
            title=title,
            chart_type=chart_type,
            created_at=(
                created_at
                or datetime.now(UTC)
            ),
            labels=labels,
            scores=scores,
            average_score=(
                average_score
                if average_score is not None
                else self._average_score_calculator.calculate(
                    scores=scores,
                )
            ),
            trend_direction=(
                trend_direction
                or self._trend_direction_detector.detect(
                    scores=scores,
                )
            ),
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            series_name=series_name,
            experiment_id=experiment_id,
            run_id=run_id,
            benchmark_id=benchmark_id,
            model_name=model_name,
            description=description,
            metadata=metadata,
        )

    def build_from_trend(
        self,
        *,
        trend: ExperimentTrendResult,
        chart_type: str = "line",
        title: str | None = None,
        labels: tuple[
            str,
            ...,
        ] | None = None,
        scores: tuple[
            float,
            ...,
        ] | None = None,
        description: str | None = None,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> VisualAnalyticsSnapshot:
        resolved_scores = (
            scores
            or self._trend_visual_mapper.scores(
                trend=trend,
            )
        )

        resolved_labels = (
            labels
            or self._trend_visual_mapper.labels(
                trend=trend,
                score_count=len(
                    resolved_scores,
                ),
            )
        )

        return self.build(
            title=self._trend_visual_mapper.title(
                trend=trend,
                override=title,
            ),
            chart_type=chart_type,
            labels=resolved_labels,
            scores=resolved_scores,
            average_score=trend.average_overall_score,
            trend_direction=(
                self._trend_visual_mapper.trend_direction(
                    trend=trend,
                )
            ),
            x_axis_label="Run",
            y_axis_label="Overall Score",
            series_name=trend.experiment_name,
            experiment_id=trend.experiment_id,
            description=self._trend_visual_mapper.description(
                trend=trend,
                override=description,
            ),
            metadata=self._trend_visual_mapper.metadata(
                trend=trend,
                extra_metadata=metadata,
            ),
        )
