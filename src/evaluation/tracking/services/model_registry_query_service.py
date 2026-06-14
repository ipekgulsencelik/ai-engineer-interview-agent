from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)
from src.evaluation.tracking.enums.model_stage import (
    ModelStage,
)
from src.evaluation.tracking.ports.model_registry_store import (
    ModelRegistryStore,
)


class ModelRegistryQueryService:
    """
    Query service for model registry lookups.
    """

    def __init__(
        self,
        *,
        store: ModelRegistryStore,
    ) -> None:
        self._store = store

    def get(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry | None:
        return self._store.get(
            registry_id=registry_id,
        )

    def get_by_model_version(
        self,
        *,
        model_name: str,
        model_version: str,
    ) -> ModelRegistryEntry | None:
        return self._store.get_by_model_version(
            model_name=model_name,
            model_version=model_version,
        )

    def require_by_model_version(
        self,
        *,
        model_name: str,
        model_version: str,
    ) -> ModelRegistryEntry:
        entry = self.get_by_model_version(
            model_name=model_name,
            model_version=model_version,
        )

        if entry is None:
            raise EvaluationValidationError(
                "model registry entry not found."
            )

        return entry

    def list_by_model(
        self,
        *,
        model_name: str,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        return self._store.list_by_model(
            model_name=model_name,
        )

    def list_by_stage(
        self,
        *,
        stage: ModelStage,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        return self._store.list_by_stage(
            stage=stage,
        )

    def list_all(
        self,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        return self._store.list_all()