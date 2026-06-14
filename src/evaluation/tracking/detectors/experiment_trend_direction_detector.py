# src/evaluation/tracking/detectors/experiment_trend_direction_detector.py

from __future__ import annotations

from src.evaluation.tracking.constants.experiment_trend import (
    TREND_MIN_SAMPLE_COUNT,
    TREND_VOLATILITY_THRESHOLD,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.enums.experiment_trend_direction import (
    ExperimentTrendDirection,
)


class ExperimentTrendDirectionDetector:
    """
    Detects trend direction.
    """

    @staticmethod
    def detect(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
        overall_score_delta: float | None,
    ) -> ExperimentTrendDirection:
        if (
            not runs
            or overall_score_delta is None
        ):
            return ExperimentTrendDirection.UNKNOWN

        if len(
            runs,
        ) < TREND_MIN_SAMPLE_COUNT:
            return (
                ExperimentTrendDirectionDetector
                ._direction_from_delta(
                    overall_score_delta=overall_score_delta,
                )
            )

        scores = tuple(
            run.overall_score
            for run in runs
            if run.overall_score is not None
        )

        direction_changes = (
            ExperimentTrendDirectionDetector
            ._count_direction_changes(
                scores=scores,
            )
        )

        if (
            direction_changes
            >= TREND_VOLATILITY_THRESHOLD
        ):
            return ExperimentTrendDirection.VOLATILE

        return (
            ExperimentTrendDirectionDetector
            ._direction_from_delta(
                overall_score_delta=overall_score_delta,
            )
        )

    @staticmethod
    def _direction_from_delta(
        *,
        overall_score_delta: float,
    ) -> ExperimentTrendDirection:
        if overall_score_delta > 0:
            return ExperimentTrendDirection.IMPROVING

        if overall_score_delta < 0:
            return ExperimentTrendDirection.REGRESSING

        return ExperimentTrendDirection.STABLE

    @staticmethod
    def _count_direction_changes(
        *,
        scores: tuple[
            float,
            ...,
        ],
    ) -> int:
        direction_changes = 0

        previous_delta: float | None = None

        for previous_score, current_score in zip(
            scores,
            scores[1:],
            strict=False,
        ):
            current_delta = (
                current_score
                - previous_score
            )

            if current_delta == 0:
                continue

            if (
                previous_delta is not None
                and (
                    current_delta > 0
                    != previous_delta > 0
                )
            ):
                direction_changes += 1

            previous_delta = current_delta

        return direction_changes