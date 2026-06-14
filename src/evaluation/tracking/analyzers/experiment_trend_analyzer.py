from __future__ import annotations

from src.evaluation.tracking.calculators.experiment_run_statistics_calculator import (
    ExperimentRunStatisticsCalculator,
)
from src.evaluation.tracking.calculators.experiment_trend_delta_calculator import (
    ExperimentTrendDeltaCalculator,
)
from src.evaluation.tracking.detectors.experiment_trend_direction_detector import (
    ExperimentTrendDirectionDetector,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.interpreters.experiment_trend_interpreter import (
    ExperimentTrendInterpreter,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class ExperimentTrendAnalyzer:
    """
    Analyzes score and pass-rate trends across
    experiment runs.
    """

    def __init__(
        self,
        *,
        delta_calculator: ExperimentTrendDeltaCalculator | None = None,
        statistics_calculator: (
            ExperimentRunStatisticsCalculator | None
        ) = None,
        direction_detector: (
            ExperimentTrendDirectionDetector | None
        ) = None,
        interpreter: ExperimentTrendInterpreter | None = None,
    ) -> None:
        self._delta_calculator = (
            delta_calculator
            or ExperimentTrendDeltaCalculator()
        )
        self._statistics_calculator = (
            statistics_calculator
            or ExperimentRunStatisticsCalculator()
        )
        self._direction_detector = (
            direction_detector
            or ExperimentTrendDirectionDetector()
        )
        self._interpreter = (
            interpreter
            or ExperimentTrendInterpreter()
        )

    def analyze(
        self,
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
        notes: str | None = None,
    ) -> ExperimentTrendResult:
        if not runs:
            raise ValueError(
                "runs cannot be empty."
            )

        sorted_runs = tuple(
            sorted(
                runs,
                key=lambda run: run.started_at,
            )
        )

        first_run = sorted_runs[0]
        latest_run = sorted_runs[-1]

        scored_runs = tuple(
            run
            for run in sorted_runs
            if run.overall_score is not None
        )

        overall_score_delta = (
            self._delta_calculator.calculate(
                first_value=first_run.overall_score,
                latest_value=latest_run.overall_score,
            )
        )

        pass_rate_delta = (
            self._delta_calculator.calculate(
                first_value=first_run.pass_rate,
                latest_value=latest_run.pass_rate,
            )
        )

        best_run = self._statistics_calculator.best_run(
            runs=scored_runs,
        )

        worst_run = self._statistics_calculator.worst_run(
            runs=scored_runs,
        )

        average_overall_score = (
            self._statistics_calculator.average_score(
                runs=scored_runs,
            )
        )

        trend_direction = self._direction_detector.detect(
            runs=scored_runs,
            overall_score_delta=overall_score_delta,
        )

        return ExperimentTrendResult(
            experiment_id=latest_run.experiment_id,
            experiment_name=latest_run.experiment_name,
            experiment_version=latest_run.experiment_version,
            run_count=len(
                sorted_runs,
            ),
            first_run_id=first_run.run_id,
            latest_run_id=latest_run.run_id,
            first_overall_score=first_run.overall_score,
            latest_overall_score=latest_run.overall_score,
            average_overall_score=average_overall_score,
            overall_score_delta=overall_score_delta,
            first_pass_rate=first_run.pass_rate,
            latest_pass_rate=latest_run.pass_rate,
            pass_rate_delta=pass_rate_delta,
            best_run_id=(
                None
                if best_run is None
                else best_run.run_id
            ),
            best_overall_score=(
                None
                if best_run is None
                else best_run.overall_score
            ),
            worst_run_id=(
                None
                if worst_run is None
                else worst_run.run_id
            ),
            worst_overall_score=(
                None
                if worst_run is None
                else worst_run.overall_score
            ),
            trend_direction=trend_direction,
            interpretation=self._interpreter.interpret(
                trend_direction=trend_direction,
            ),
            notes=notes,
        )