from __future__ import annotations

from src.evaluation.rag.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentLineageDiffService:
    """
    Compares two experiment lineage nodes.
    """

    @staticmethod
    def score_delta(
        *,
        baseline: ExperimentNode,
        candidate: ExperimentNode,
    ) -> float | None:
        if (
            baseline.overall_score is None
            or candidate.overall_score is None
        ):
            return None

        return (
            candidate.overall_score
            - baseline.overall_score
        )

    @staticmethod
    def pass_rate_delta(
        *,
        baseline: ExperimentNode,
        candidate: ExperimentNode,
    ) -> float | None:
        if (
            baseline.pass_rate is None
            or candidate.pass_rate is None
        ):
            return None

        return (
            candidate.pass_rate
            - baseline.pass_rate
        )

    @staticmethod
    def sample_count_delta(
        *,
        baseline: ExperimentNode,
        candidate: ExperimentNode,
    ) -> int | None:
        if (
            baseline.sample_count is None
            or candidate.sample_count is None
        ):
            return None

        return (
            candidate.sample_count
            - baseline.sample_count
        )