from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)
from src.evaluation.tracking.enums.model_stage import (
    ModelStage,
)


class ModelRegistryStore(
    ABC,
):
    """
    Store port for model registry persistence.
    """

    @abstractmethod
    def save(
        self,
        *,
        entry: ModelRegistryEntry,
    ) -> None:
        """
        Persists a model registry entry.
        """

    @abstractmethod
    def update(
        self,
        *,
        entry: ModelRegistryEntry,
    ) -> None:
        """
        Updates a model registry entry.
        """

    @abstractmethod
    def get_by_id(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry | None:
        """
        Returns model registry entry by id.
        """

    @abstractmethod
    def get_by_model_version(
        self,
        *,
        model_name: str,
        model_version: str,
    ) -> ModelRegistryEntry | None:
        """
        Returns model registry entry by model name and version.
        """

    @abstractmethod
    def list_by_model(
        self,
        *,
        model_name: str,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        """
        Lists all versions for one model.
        """

    @abstractmethod
    def list_by_stage(
        self,
        *,
        stage: ModelStage,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        """
        Lists model registry entries by lifecycle stage.
        """

    @abstractmethod
    def list_all(
        self,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        """
        Lists all model registry entries.
        """

    @abstractmethod
    def exists(
        self,
        *,
        registry_id: str,
    ) -> bool:
        """
        Returns whether registry entry exists.
        """

    @abstractmethod
    def exists_model_version(
        self,
        *,
        model_name: str,
        model_version: str,
    ) -> bool:
        """
        Returns whether model name and version exists.
        """