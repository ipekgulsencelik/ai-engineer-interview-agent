from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)


class ExternalModelRegistryClient(
    ABC,
):
    """
    Client port for external model registry tracking.
    """

    @abstractmethod
    async def register_model(
        self,
        *,
        model: ModelRegistryEntry,
    ) -> None:
        """
        Registers model metadata in the external system.
        """