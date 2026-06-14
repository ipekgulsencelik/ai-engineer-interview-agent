from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.artifact_version import (
    ArtifactVersion,
)


class ArtifactVersionStore(
    ABC,
):
    """
    Store port for artifact version persistence.

    Infrastructure adapters should implement this
    interface for database, filesystem metadata,
    object storage, or artifact registry backed
    version tracking.
    """

    @abstractmethod
    def save(
        self,
        *,
        version: ArtifactVersion,
    ) -> None:
        """
        Persists an artifact version.
        """

    @abstractmethod
    def get_by_id(
        self,
        *,
        version_id: str,
    ) -> ArtifactVersion | None:
        """
        Returns artifact version by version id.
        """

    @abstractmethod
    def get_latest(
        self,
        *,
        artifact_id: str,
    ) -> ArtifactVersion | None:
        """
        Returns latest version for one artifact.
        """

    @abstractmethod
    def list_by_artifact(
        self,
        *,
        artifact_id: str,
    ) -> tuple[
        ArtifactVersion,
        ...,
    ]:
        """
        Lists all versions for one artifact.
        """

    @abstractmethod
    def exists(
        self,
        *,
        version_id: str,
    ) -> bool:
        """
        Returns whether version exists.
        """

    @abstractmethod
    def delete(
        self,
        *,
        version_id: str,
    ) -> None:
        """
        Deletes artifact version metadata.
        """