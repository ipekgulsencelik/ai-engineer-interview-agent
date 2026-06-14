from __future__ import annotations

from src.evaluation.rag.services.experiment_lineage_diff_service import ExperimentLineageDiffService
from tests.evaluation.rag.factories import experiment_node


def test_experiment_lineage_diff_service_should_calculate_score_pass_rate_and_sample_count_deltas() -> None:
    baseline = experiment_node(overall_score=0.5, pass_rate=0.6, sample_count=10, passed_count=6, failed_count=4)
    candidate = experiment_node(experiment_id="candidate", overall_score=0.8, pass_rate=0.9, sample_count=12, passed_count=11, failed_count=1)

    assert ExperimentLineageDiffService.score_delta(baseline=baseline, candidate=candidate) == 0.30000000000000004
    assert ExperimentLineageDiffService.pass_rate_delta(baseline=baseline, candidate=candidate) == 0.30000000000000004
    assert ExperimentLineageDiffService.sample_count_delta(baseline=baseline, candidate=candidate) == 2
