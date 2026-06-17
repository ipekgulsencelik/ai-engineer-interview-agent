from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class MLflowClient(
    ABC,
):
    """
    MLflow delivery port.

    Infrastructure adapters should implement this
    interface using MLflow Tracking APIs.
    """

    @abstractmethod
    def log_artifact(
        self,
        *,
        run_id: str,
        local_path: str,
        artifact_path: str | None = None,
    ) -> None:
        """
        Logs a local artifact file to an MLflow run.
        """

    @abstractmethod
    def set_tag(
        self,
        *,
        run_id: str,
        key: str,
        value: str,
    ) -> None:
        """
        Sets an MLflow run tag.
        """