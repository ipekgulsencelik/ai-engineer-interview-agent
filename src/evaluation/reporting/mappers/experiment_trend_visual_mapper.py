from __future__ import annotations

from src.evaluation.reporting.mappers.summary_trend_direction_mapper import (
    SummaryTrendDirectionMapper,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class ExperimentTrendVisualMapper:
    """
    Maps experiment trend results to visual analytics data.
    """

    def __init__(
        self,
        *,
        trend_direction_mapper: (
            SummaryTrendDirectionMapper | None
        ) = None,
    ) -> None:
        self._trend_direction_mapper = (
            trend_direction_mapper
            or SummaryTrendDirectionMapper()
        )

    def scores(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> tuple[
        float,
        ...,
    ]:
        scores: list[
            float
        ] = []

        if trend.first_overall_score is not None:
            scores.append(
                trend.first_overall_score,
            )

        if (
            trend.latest_overall_score is not None
            and trend.latest_run_id != trend.first_run_id
        ):
            scores.append(
                trend.latest_overall_score,
            )

        return tuple(
            scores,
        )

    @staticmethod
    def labels(
        *,
        trend: ExperimentTrendResult,
        score_count: int,
    ) -> tuple[
        str,
        ...,
    ]:
        if score_count == 0:
            return ()

        if score_count == 1:
            return (
                trend.first_run_id,
            )

        return (
            trend.first_run_id,
            trend.latest_run_id,
        )

    def trend_direction(
        self,
        *,
        trend: ExperimentTrendResult,
    ):
        return self._trend_direction_mapper.from_string(
            direction=str(
                trend.trend_direction,
            ),
        )

    @staticmethod
    def title(
        *,
        trend: ExperimentTrendResult,
        override: str | None = None,
    ) -> str:
        if override is not None:
            return override

        return (
            "Experiment Trend - "
            f"{trend.experiment_name}"
        )

    @staticmethod
    def description(
        *,
        trend: ExperimentTrendResult,
        override: str | None = None,
    ) -> str:
        return (
            override
            or trend.interpretation
        )

    @staticmethod
    def metadata(
        *,
        trend: ExperimentTrendResult,
        extra_metadata: dict[str, str] | None = None,
    ) -> dict[str, str]:
        return {
            **(
                extra_metadata
                or {}
            ),
            "experiment_version": trend.experiment_version,
            "first_run_id": trend.first_run_id,
            "latest_run_id": trend.latest_run_id,
            "run_count": str(
                trend.run_count,
            ),
        }
