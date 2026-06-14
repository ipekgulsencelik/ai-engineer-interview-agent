from __future__ import annotations

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class ExperimentRunQueryFilter:
    """
    Applies ExperimentQuery filters to experiment runs.
    """

    @staticmethod
    def apply(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        return tuple(
            run
            for run in runs
            if ExperimentRunQueryFilter.matches(
                run=run,
                query=query,
            )
        )

    @staticmethod
    def matches(
        *,
        run: ExperimentRun,
        query: ExperimentQuery,
    ) -> bool:
        equality_checks = (
            (
                query.experiment_id,
                run.experiment_id,
            ),
            (
                query.run_id,
                run.run_id,
            ),
            (
                query.experiment_name,
                run.experiment_name,
            ),
            (
                query.experiment_version,
                run.experiment_version,
            ),
            (
                query.dataset_id,
                run.dataset_id,
            ),
            (
                query.dataset_name,
                run.dataset_name,
            ),
            (
                query.dataset_version,
                run.dataset_version,
            ),
            (
                query.benchmark_id,
                run.benchmark_id,
            ),
            (
                query.benchmark_name,
                run.benchmark_name,
            ),
            (
                query.benchmark_version,
                run.benchmark_version,
            ),
            (
                query.model_name,
                run.model_name,
            ),
            (
                query.retriever_name,
                run.retriever_name,
            ),
            (
                query.evaluator_name,
                run.evaluator_name,
            ),
            (
                query.status,
                run.status,
            ),
        )

        for expected, actual in equality_checks:
            if (
                expected is not None
                and actual != expected
            ):
                return False

        if (
            query.created_after is not None
            and run.started_at < query.created_after
        ):
            return False

        if (
            query.created_before is not None
            and run.started_at > query.created_before
        ):
            return False

        if not ExperimentRunQueryFilter._score_in_range(
            value=run.overall_score,
            minimum=query.min_overall_score,
            maximum=query.max_overall_score,
        ):
            return False

        if not ExperimentRunQueryFilter._score_in_range(
            value=run.pass_rate,
            minimum=query.min_pass_rate,
            maximum=query.max_pass_rate,
        ):
            return False

        return True

    @staticmethod
    def _score_in_range(
        *,
        value: float | None,
        minimum: float | None,
        maximum: float | None,
    ) -> bool:
        if minimum is not None:
            if (
                value is None
                or value < minimum
            ):
                return False

        if maximum is not None:
            if (
                value is None
                or value > maximum
            ):
                return False

        return True