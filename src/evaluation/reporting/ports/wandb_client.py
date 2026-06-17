from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class WandbClient(
    ABC,
):
    """
    Weights & Biases delivery port.
    """

    @abstractmethod
    def log_artifact(
        self,
        *,
        run_id: str,
        artifact_path: str,
        artifact_name: str,
        artifact_type: str,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """
        Logs a report artifact to a W&B run.
        """

    @abstractmethod
    def log_summary(
        self,
        *,
        run_id: str,
        values: dict[str, object],
    ) -> None:
        """
        Logs report metadata or summary values to a W&B run.
        """