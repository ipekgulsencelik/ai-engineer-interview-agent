from __future__ import annotations

import sqlite3
from pathlib import Path

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.repositories.experiment_repository import (
    ExperimentRepository,
)
from src.evaluation.tracking.repositories.sqlite.sqlite_experiment_mapper import (
    SQLiteExperimentMapper,
)
from src.evaluation.tracking.repositories.sqlite.sqlite_experiment_paginator import (
    SQLiteExperimentPaginator,
)
from src.evaluation.tracking.repositories.sqlite.sqlite_experiment_query_builder import (
    SQLiteExperimentQueryBuilder,
)
from src.evaluation.tracking.repositories.sqlite.sqlite_experiment_schema_initializer import (
    SQLiteExperimentSchemaInitializer,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class SQLiteExperimentRepository(
    ExperimentRepository,
):
    """
    SQLite implementation of ExperimentRepository.
    """

    def __init__(
        self,
        *,
        database_path: str | Path,
        mapper: SQLiteExperimentMapper | None = None,
        query_builder: (
            SQLiteExperimentQueryBuilder | None
        ) = None,
        paginator: SQLiteExperimentPaginator | None = None,
        schema_initializer: (
            SQLiteExperimentSchemaInitializer | None
        ) = None,
    ) -> None:
        self._database_path = str(
            database_path,
        )
        self._mapper = (
            mapper
            or SQLiteExperimentMapper()
        )
        self._query_builder = (
            query_builder
            or SQLiteExperimentQueryBuilder()
        )
        self._paginator = (
            paginator
            or SQLiteExperimentPaginator()
        )
        self._schema_initializer = (
            schema_initializer
            or SQLiteExperimentSchemaInitializer()
        )

        self._initialize()

    def save(
        self,
        *,
        experiment: ExperimentNode,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO experiments (
                    experiment_id,
                    experiment_name,
                    experiment_version,
                    parent_experiment_id,
                    dataset_id,
                    dataset_name,
                    dataset_version,
                    benchmark_id,
                    benchmark_name,
                    benchmark_version,
                    model_name,
                    retriever_name,
                    evaluator_name,
                    overall_score,
                    pass_rate,
                    sample_count,
                    passed_count,
                    failed_count,
                    tags,
                    created_at,
                    notes
                )
                VALUES (
                    :experiment_id,
                    :experiment_name,
                    :experiment_version,
                    :parent_experiment_id,
                    :dataset_id,
                    :dataset_name,
                    :dataset_version,
                    :benchmark_id,
                    :benchmark_name,
                    :benchmark_version,
                    :model_name,
                    :retriever_name,
                    :evaluator_name,
                    :overall_score,
                    :pass_rate,
                    :sample_count,
                    :passed_count,
                    :failed_count,
                    :tags,
                    :created_at,
                    :notes
                )
                """,
                self._mapper.to_record(
                    experiment=experiment,
                ),
            )

    def update(
        self,
        *,
        experiment: ExperimentNode,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE experiments
                SET
                    experiment_name = :experiment_name,
                    experiment_version = :experiment_version,
                    parent_experiment_id = :parent_experiment_id,
                    dataset_id = :dataset_id,
                    dataset_name = :dataset_name,
                    dataset_version = :dataset_version,
                    benchmark_id = :benchmark_id,
                    benchmark_name = :benchmark_name,
                    benchmark_version = :benchmark_version,
                    model_name = :model_name,
                    retriever_name = :retriever_name,
                    evaluator_name = :evaluator_name,
                    overall_score = :overall_score,
                    pass_rate = :pass_rate,
                    sample_count = :sample_count,
                    passed_count = :passed_count,
                    failed_count = :failed_count,
                    tags = :tags,
                    created_at = :created_at,
                    notes = :notes
                WHERE experiment_id = :experiment_id
                """,
                self._mapper.to_record(
                    experiment=experiment,
                ),
            )

    def get_by_id(
        self,
        *,
        experiment_id: str,
    ) -> ExperimentNode | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM experiments
                WHERE experiment_id = ?
                """,
                (
                    experiment_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._mapper.to_entity(
            row=row,
        )

    def list_all(
        self,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        return self._fetch_many(
            sql="""
                SELECT *
                FROM experiments
                ORDER BY created_at DESC
            """,
            parameters=(),
        )

    def list_by_name(
        self,
        *,
        experiment_name: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        return self._fetch_many(
            sql="""
                SELECT *
                FROM experiments
                WHERE experiment_name = ?
                ORDER BY created_at DESC
            """,
            parameters=(
                experiment_name,
            ),
        )

    def list_by_version(
        self,
        *,
        experiment_version: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        return self._fetch_many(
            sql="""
                SELECT *
                FROM experiments
                WHERE experiment_version = ?
                ORDER BY created_at DESC
            """,
            parameters=(
                experiment_version,
            ),
        )

    def search(
        self,
        *,
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        sql, parameters = self._query_builder.build_search(
            query=query,
        )

        experiments = self._fetch_many(
            sql=sql,
            parameters=parameters,
        )

        return self._paginator.paginate(
            experiments=experiments,
            query=query,
        )

    def exists(
        self,
        *,
        experiment_id: str,
    ) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM experiments
                WHERE experiment_id = ?
                LIMIT 1
                """,
                (
                    experiment_id,
                ),
            ).fetchone()

        return row is not None

    def delete(
        self,
        *,
        experiment_id: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM experiments
                WHERE experiment_id = ?
                """,
                (
                    experiment_id,
                ),
            )

    def _initialize(
        self,
    ) -> None:
        with self._connect() as connection:
            self._schema_initializer.initialize(
                connection=connection,
            )

    def _connect(
        self,
    ) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self._database_path,
        )
        connection.row_factory = sqlite3.Row

        return connection

    def _fetch_many(
        self,
        *,
        sql: str,
        parameters: tuple[
            object,
            ...,
        ],
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        with self._connect() as connection:
            rows = connection.execute(
                sql,
                parameters,
            ).fetchall()

        return tuple(
            self._mapper.to_entity(
                row=row,
            )
            for row in rows
        )