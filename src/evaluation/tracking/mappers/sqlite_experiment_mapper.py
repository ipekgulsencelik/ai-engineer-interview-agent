from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)


class SQLiteExperimentMapper:
    """
    Maps ExperimentNode entities to and from SQLite records.
    """

    @staticmethod
    def to_record(
        *,
        experiment: ExperimentNode,
    ) -> dict[
        str,
        Any,
    ]:
        return {
            "experiment_id": experiment.experiment_id,
            "experiment_name": experiment.experiment_name,
            "experiment_version": experiment.experiment_version,
            "parent_experiment_id": experiment.parent_experiment_id,
            "dataset_id": experiment.dataset_id,
            "dataset_name": experiment.dataset_name,
            "dataset_version": experiment.dataset_version,
            "benchmark_id": experiment.benchmark_id,
            "benchmark_name": experiment.benchmark_name,
            "benchmark_version": experiment.benchmark_version,
            "model_name": experiment.model_name,
            "retriever_name": experiment.retriever_name,
            "evaluator_name": experiment.evaluator_name,
            "overall_score": experiment.overall_score,
            "pass_rate": experiment.pass_rate,
            "sample_count": experiment.sample_count,
            "passed_count": experiment.passed_count,
            "failed_count": experiment.failed_count,
            "tags": json.dumps(
                experiment.tags,
            ),
            "created_at": experiment.created_at.isoformat(),
            "notes": experiment.notes,
        }

    @staticmethod
    def to_entity(
        *,
        row: sqlite3.Row,
    ) -> ExperimentNode:
        return ExperimentNode(
            experiment_id=row["experiment_id"],
            experiment_name=row["experiment_name"],
            experiment_version=row["experiment_version"],
            parent_experiment_id=row["parent_experiment_id"],
            dataset_id=row["dataset_id"],
            dataset_name=row["dataset_name"],
            dataset_version=row["dataset_version"],
            benchmark_id=row["benchmark_id"],
            benchmark_name=row["benchmark_name"],
            benchmark_version=row["benchmark_version"],
            model_name=row["model_name"],
            retriever_name=row["retriever_name"],
            evaluator_name=row["evaluator_name"],
            overall_score=row["overall_score"],
            pass_rate=row["pass_rate"],
            sample_count=row["sample_count"],
            passed_count=row["passed_count"],
            failed_count=row["failed_count"],
            tags=tuple(
                json.loads(
                    row["tags"],
                )
            ),
            created_at=datetime.fromisoformat(
                row["created_at"],
            ),
            notes=row["notes"],
        )