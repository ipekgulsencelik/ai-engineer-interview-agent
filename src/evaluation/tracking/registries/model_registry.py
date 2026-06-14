from __future__ import annotations

from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)
from src.evaluation.tracking.enums.model_stage import (
    ModelStage,
)
from src.evaluation.tracking.services.model_registry_query_service import (
    ModelRegistryQueryService,
)
from src.evaluation.tracking.services.model_registry_service import (
    ModelRegistryService,
)
from src.evaluation.tracking.stores.model_registry_store import (
    ModelRegistryStore,
)


class ModelRegistry:
    """
    Facade for model registry operations.
    """

    def __init__(
        self,
        *,
        store: ModelRegistryStore,
        service: ModelRegistryService | None = None,
        query_service: (
            ModelRegistryQueryService | None
        ) = None,
    ) -> None:
        self._service = (
            service
            or ModelRegistryService(
                store=store,
            )
        )

        self._query_service = (
            query_service
            or ModelRegistryQueryService(
                store=store,
            )
        )

    def register(
        self,
        *,
        entry: ModelRegistryEntry,
    ) -> ModelRegistryEntry:
        return self._service.register(
            entry=entry,
        )

    def promote_to_staging(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self._service.promote_to_staging(
            registry_id=registry_id,
        )

    def promote_to_canary(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self._service.promote_to_canary(
            registry_id=registry_id,
        )

    def promote_to_production(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self._service.promote_to_production(
            registry_id=registry_id,
        )

    def archive(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry:
        return self._service.archive(
            registry_id=registry_id,
        )

    def update_stage(
        self,
        *,
        registry_id: str,
        stage: ModelStage,
    ) -> ModelRegistryEntry:
        return self._service.update_stage(
            registry_id=registry_id,
            stage=stage,
        )

    def get(
        self,
        *,
        registry_id: str,
    ) -> ModelRegistryEntry | None:
        return self._query_service.get(
            registry_id=registry_id,
        )

    def get_by_model_version(
        self,
        *,
        model_name: str,
        model_version: str,
    ) -> ModelRegistryEntry | None:
        return self._query_service.get_by_model_version(
            model_name=model_name,
            model_version=model_version,
        )

    def require_by_model_version(
        self,
        *,
        model_name: str,
        model_version: str,
    ) -> ModelRegistryEntry:
        return (
            self._query_service.require_by_model_version(
                model_name=model_name,
                model_version=model_version,
            )
        )

    def list_by_model(
        self,
        *,
        model_name: str,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        return self._query_service.list_by_model(
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
        return self._query_service.list_by_stage(
            stage=stage,
        )

    def list_all(
        self,
    ) -> tuple[
        ModelRegistryEntry,
        ...,
    ]:
        return self._query_service.list_all()