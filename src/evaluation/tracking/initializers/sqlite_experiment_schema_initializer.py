from __future__ import annotations

import sqlite3


class SQLiteExperimentSchemaInitializer:
    """
    Initializes SQLite experiment metadata schema.
    """

    @staticmethod
    def initialize(
        *,
        connection: sqlite3.Connection,
    ) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                experiment_id TEXT PRIMARY KEY,
                experiment_name TEXT NOT NULL,
                experiment_version TEXT NOT NULL,
                parent_experiment_id TEXT,
                dataset_id TEXT,
                dataset_name TEXT,
                dataset_version TEXT,
                benchmark_id TEXT,
                benchmark_name TEXT,
                benchmark_version TEXT,
                model_name TEXT,
                retriever_name TEXT,
                evaluator_name TEXT,
                overall_score REAL,
                pass_rate REAL,
                sample_count INTEGER,
                passed_count INTEGER,
                failed_count INTEGER,
                tags TEXT NOT NULL,
                created_at TEXT NOT NULL,
                notes TEXT
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_experiments_name
            ON experiments (experiment_name)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_experiments_version
            ON experiments (experiment_version)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_experiments_created_at
            ON experiments (created_at)
            """
        )