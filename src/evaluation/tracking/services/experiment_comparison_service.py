from __future__ import annotations

from src.evaluation.tracking.calculators.experiment_delta_calculator import (
    ExperimentDeltaCalculator,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.interpreters.experiment_comparison_interpreter import (
    ExperimentComparisonInterpreter,
)
from src.evaluation.tracking.selectors.experiment_winner_selector import (
    ExperimentWinnerSelector,
)
from src.evaluation.tracking.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)


class ExperimentComparisonService:
    """
    Compares baseline and candidate experiment runs.
    """

    def __init__(
        self,
        *,
        delta_calculator: ExperimentDeltaCalculator | None = None,
        winner_selector: ExperimentWinnerSelector | None = None,
        interpreter: ExperimentComparisonInterpreter | None = None,
    ) -> None:
        self._delta_calculator = (
            delta_calculator
            or ExperimentDeltaCalculator()
        )
        self._winner_selector = (
            winner_selector
            or ExperimentWinnerSelector()
        )
        self._interpreter = (
            interpreter
            or ExperimentComparisonInterpreter()
        )

    def compare(
        self,
        *,
        baseline: ExperimentRun,
        candidate: ExperimentRun,
        notes: str | None = None,
    ) -> ExperimentComparisonResult:
        overall_score_delta = self._delta_calculator.float_delta(
            baseline_value=baseline.overall_score,
            candidate_value=candidate.overall_score,
        )

        pass_rate_delta = self._delta_calculator.float_delta(
            baseline_value=baseline.pass_rate,
            candidate_value=candidate.pass_rate,
        )

        sample_count_delta = self._delta_calculator.int_delta(
            baseline_value=baseline.sample_count,
            candidate_value=candidate.sample_count,
        )

        return ExperimentComparisonResult(
            baseline_run_id=baseline.run_id,
            candidate_run_id=candidate.run_id,
            baseline_experiment_id=baseline.experiment_id,
            candidate_experiment_id=candidate.experiment_id,
            baseline_experiment_name=baseline.experiment_name,
            candidate_experiment_name=candidate.experiment_name,
            baseline_experiment_version=(
                baseline.experiment_version
            ),
            candidate_experiment_version=(
                candidate.experiment_version
            ),
            baseline_overall_score=baseline.overall_score,
            candidate_overall_score=candidate.overall_score,
            overall_score_delta=overall_score_delta,
            baseline_pass_rate=baseline.pass_rate,
            candidate_pass_rate=candidate.pass_rate,
            pass_rate_delta=pass_rate_delta,
            baseline_sample_count=baseline.sample_count,
            candidate_sample_count=candidate.sample_count,
            sample_count_delta=sample_count_delta,
            winner_experiment_id=(
                self._winner_selector.select(
                    baseline=baseline,
                    candidate=candidate,
                )
            ),
            interpretation=(
                self._interpreter.interpret(
                    overall_score_delta=overall_score_delta,
                    pass_rate_delta=pass_rate_delta,
                )
            ),
            notes=notes,
        )