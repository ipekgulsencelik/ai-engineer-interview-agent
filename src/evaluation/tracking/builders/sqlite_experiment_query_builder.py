from __future__ import annotations

from typing import Any

from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class SQLiteExperimentQueryBuilder:
    """
    Builds SQLite search SQL for experiment queries.
    """

    def build_search(
        self,
        *,
        query: ExperimentQuery,
    ) -> tuple[
        str,
        tuple[
            Any,
            ...,
        ],
    ]:
        conditions: list[
            str
        ] = []
        parameters: list[
            Any
        ] = []

        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="experiment_id",
            value=query.experiment_id,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="experiment_name",
            value=query.experiment_name,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="experiment_version",
            value=query.experiment_version,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="dataset_id",
            value=query.dataset_id,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="dataset_name",
            value=query.dataset_name,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="dataset_version",
            value=query.dataset_version,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="benchmark_id",
            value=query.benchmark_id,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="benchmark_name",
            value=query.benchmark_name,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="benchmark_version",
            value=query.benchmark_version,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="model_name",
            value=query.model_name,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="retriever_name",
            value=query.retriever_name,
        )
        self._add_exact_filter(
            conditions=conditions,
            parameters=parameters,
            column="evaluator_name",
            value=query.evaluator_name,
        )

        self._add_range_filter(
            conditions=conditions,
            parameters=parameters,
            column="created_at",
            operator=">=",
            value=(
                None
                if query.created_after is None
                else query.created_after.isoformat()
            ),
        )
        self._add_range_filter(
            conditions=conditions,
            parameters=parameters,
            column="created_at",
            operator="<=",
            value=(
                None
                if query.created_before is None
                else query.created_before.isoformat()
            ),
        )
        self._add_range_filter(
            conditions=conditions,
            parameters=parameters,
            column="overall_score",
            operator=">=",
            value=query.min_overall_score,
        )
        self._add_range_filter(
            conditions=conditions,
            parameters=parameters,
            column="overall_score",
            operator="<=",
            value=query.max_overall_score,
        )
        self._add_range_filter(
            conditions=conditions,
            parameters=parameters,
            column="pass_rate",
            operator=">=",
            value=query.min_pass_rate,
        )
        self._add_range_filter(
            conditions=conditions,
            parameters=parameters,
            column="pass_rate",
            operator="<=",
            value=query.max_pass_rate,
        )

        sql = """
            SELECT *
            FROM experiments
        """

        if conditions:
            sql += (
                " WHERE "
                + " AND ".join(
                    conditions,
                )
            )

        sql += " ORDER BY created_at DESC"

        return (
            sql,
            tuple(
                parameters,
            ),
        )

    @staticmethod
    def _add_exact_filter(
        *,
        conditions: list[
            str,
        ],
        parameters: list[
            Any,
        ],
        column: str,
        value: str | None,
    ) -> None:
        if value is None:
            return

        conditions.append(
            f"{column} = ?"
        )
        parameters.append(
            value,
        )

    @staticmethod
    def _add_range_filter(
        *,
        conditions: list[
            str,
        ],
        parameters: list[
            Any,
        ],
        column: str,
        operator: str,
        value: Any | None,
    ) -> None:
        if value is None:
            return

        conditions.append(
            f"{column} {operator} ?"
        )
        parameters.append(
            value,
        )