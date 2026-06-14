from __future__ import annotations

from dataclasses import replace

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


class ModelRegistryService:
    """
    Application service for model registry operations.
    """

    def __init__(
        self,
        *,
        store: ModelRegistryStore,
    ) -> None:
        self._store = store

    def register(
        self,
        *,
        entry: ModelRegistryEntry,
    ) -> ModelRegistryEntry:
        if self._store.exists_model_version(
            model_name=entry.model_name,
            model_version=entry.model_version,
        ):
            raise EvaluationValidationError(
                "model registry entry already exists."
            )

        self._store.save(
            entry=entry,
        )

        return entry

    def update_stage(
        self,
        *,
        registry_id: str,
        stage: ModelStage,
    ) -> ModelRegistryEntry:
        entry = self._get_required(
            registry_id=registry_id,
        )

        updated_entry = replace(
            entry,
            stage=stage,
        )

        self._store.update(
            entry=updated_entry,
        )

        return updated_entry

    def archive(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self.update_stage(
            registry_id=registry_id,
            stage=ModelStage.ARCHIVED,
        )

    def promote_to_staging(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self.update_stage(
            registry_id=registry_id,
            stage=ModelStage.STAGING,
        )

    def promote_to_canary(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self.update_stage(
            registry_id=registry_id,
            stage=ModelStage.CANARY,
        )

    def promote_to_production(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self.update_stage(
            registry_id=registry_id,
            stage=ModelStage.PRODUCTION,
        )

    def get(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry | None:
        return self._store.get_by_id(
            registry_id=registry_id,
        )

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

    def _get_required(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        entry = self._store.get_by_id(
            registry_id=registry_id,
        )

        if entry is None:
            raise EvaluationValidationError(
                "model registry entry not found."
            )

        return entry