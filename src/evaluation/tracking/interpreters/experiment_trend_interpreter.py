from __future__ import annotations

from src.evaluation.tracking.constants.experiment_trend_messages import (
    EXPERIMENT_TREND_IMPROVING,
    EXPERIMENT_TREND_REGRESSING,
    EXPERIMENT_TREND_STABLE,
    EXPERIMENT_TREND_UNKNOWN,
    EXPERIMENT_TREND_VOLATILE,
)
from src.evaluation.tracking.enums.experiment_trend_direction import (
    ExperimentTrendDirection,
)


class ExperimentTrendInterpreter:
    """
    Interprets trend direction.
    """

    @staticmethod
    def interpret(
        *,
        trend_direction: ExperimentTrendDirection,
    ) -> str:
        mapping = {
            ExperimentTrendDirection.IMPROVING: (
                EXPERIMENT_TREND_IMPROVING
            ),
            ExperimentTrendDirection.REGRESSING: (
                EXPERIMENT_TREND_REGRESSING
            ),
            ExperimentTrendDirection.VOLATILE: (
                EXPERIMENT_TREND_VOLATILE
            ),
            ExperimentTrendDirection.STABLE: (
                EXPERIMENT_TREND_STABLE
            ),
            ExperimentTrendDirection.UNKNOWN: (
                EXPERIMENT_TREND_UNKNOWN
            ),
        }

        return mapping[
            trend_direction
        ]