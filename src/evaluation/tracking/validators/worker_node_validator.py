from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.entities.worker_node import (
    WorkerNode,
)
from src.evaluation.tracking.registries.worker_node_registry import (
    WorkerNodeRegistry,
)


class WorkerNodeValidator:
    """
    Validates worker node lifecycle and job rules.
    """

    @staticmethod
    def ensure_not_registered(
        *,
        registry: WorkerNodeRegistry,
        node_id: str,
    ) -> None:
        if registry.exists(
            node_id=node_id,
        ):
            raise EvaluationValidationError(
                "worker node already registered."
            )

    @staticmethod
    def require_registered(
        *,
        registry: WorkerNodeRegistry,
        node_id: str,
    ) -> WorkerNode:
        worker = registry.get(
            node_id=node_id,
        )

        if worker is None:
            raise EvaluationValidationError(
                "worker node not registered."
            )

        return worker

    @staticmethod
    def ensure_can_receive_job(
        *,
        worker: WorkerNode,
    ) -> None:
        if not worker.active:
            raise EvaluationValidationError(
                "only active workers can receive jobs."
            )

        if worker.current_job_id is not None:
            raise EvaluationValidationError(
                "worker already has an active job."
            )

    @staticmethod
    def ensure_current_job(
        *,
        worker: WorkerNode,
        job_id: str,
    ) -> None:
        if worker.current_job_id != job_id:
            raise EvaluationValidationError(
                "job_id does not match worker current job."
            )