from __future__ import annotations

from src.evaluation.ops.exporters.json_serialization_utils import (
    JSONSerializationUtils,
)
from src.evaluation.ops.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)


class ExperimentComparisonJSONRenderer:
    """
    Renders experiment comparison results as JSON.
    """

    def __init__(
        self,
        *,
        utils: JSONSerializationUtils | None = None,
    ) -> None:
        self._utils = utils or JSONSerializationUtils()

    def render(
        self,
        *,
        comparison: ExperimentComparisonResult,
    ) -> str:
        return self._utils.to_json(
            payload={
                "baseline_run_id": comparison.baseline_run_id,
                "candidate_run_id": comparison.candidate_run_id,
                "baseline_experiment_id": (
                    comparison.baseline_experiment_id
                ),
                "candidate_experiment_id": (
                    comparison.candidate_experiment_id
                ),
                "baseline_experiment_name": (
                    comparison.baseline_experiment_name
                ),
                "candidate_experiment_name": (
                    comparison.candidate_experiment_name
                ),
                "baseline_experiment_version": (
                    comparison.baseline_experiment_version
                ),
                "candidate_experiment_version": (
                    comparison.candidate_experiment_version
                ),
                "baseline_overall_score": (
                    comparison.baseline_overall_score
                ),
                "candidate_overall_score": (
                    comparison.candidate_overall_score
                ),
                "overall_score_delta": comparison.overall_score_delta,
                "baseline_pass_rate": comparison.baseline_pass_rate,
                "candidate_pass_rate": comparison.candidate_pass_rate,
                "pass_rate_delta": comparison.pass_rate_delta,
                "baseline_sample_count": comparison.baseline_sample_count,
                "candidate_sample_count": comparison.candidate_sample_count,
                "sample_count_delta": comparison.sample_count_delta,
                "winner_experiment_id": comparison.winner_experiment_id,
                "winning_run_id": comparison.winning_run_id,
                "interpretation": comparison.interpretation,
                "notes": comparison.notes,
            },
        )