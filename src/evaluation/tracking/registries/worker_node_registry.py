from __future__ import annotations

from src.evaluation.tracking.entities.worker_node import (
    WorkerNode,
)


class WorkerNodeRegistry:
    """
    In-memory registry for worker node state.
    """

    def __init__(
        self,
    ) -> None:
        self._workers: dict[
            str,
            WorkerNode,
        ] = {}

    def add(
        self,
        *,
        worker: WorkerNode,
    ) -> None:
        self._workers[
            worker.node_id
        ] = worker

    def update(
        self,
        *,
        worker: WorkerNode,
    ) -> None:
        self._workers[
            worker.node_id
        ] = worker

    def get(
        self,
        *,
        node_id: str,
    ) -> WorkerNode | None:
        return self._workers.get(
            node_id,
        )

    def exists(
        self,
        *,
        node_id: str,
    ) -> bool:
        return node_id in self._workers

    def list_all(
        self,
    ) -> tuple[
        WorkerNode,
        ...,
    ]:
        return tuple(
            self._workers.values(),
        )

    def list_active(
        self,
    ) -> tuple[
        WorkerNode,
        ...,
    ]:
        return tuple(
            worker
            for worker in self._workers.values()
            if worker.active
        )