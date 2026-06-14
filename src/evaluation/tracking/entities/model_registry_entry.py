from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.model_stage import (
    ModelStage,
)
from src.evaluation.tracking.validators.model_registry_entry_validator import (
    ModelRegistryEntryValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ModelRegistryEntry:
    """
    Immutable model registry entry.

    Represents a registered model version and its
    associated metadata inside the evaluation
    platform registry.
    """

    registry_id: str

    model_name: str

    model_version: str

    stage: ModelStage

    created_at: datetime

    framework: str | None = None

    provider: str | None = None

    model_uri: str | None = None

    artifact_path: str | None = None

    checksum: str | None = None

    owner: str | None = None

    description: str | None = None

    tags: tuple[
        str,
        ...,
    ] = ()

    metadata: dict[
        str,
        str,
    ] | None = None

    benchmark_score: float | None = None

    def __post_init__(
        self,
    ) -> None:
        ModelRegistryEntryValidator.validate(
            registry_id=self.registry_id,
            model_name=self.model_name,
            model_version=self.model_version,
            stage=self.stage,
            created_at=self.created_at,
            framework=self.framework,
            provider=self.provider,
            model_uri=self.model_uri,
            artifact_path=self.artifact_path,
            checksum=self.checksum,
            owner=self.owner,
            description=self.description,
            tags=self.tags,
            metadata=self.metadata,
            benchmark_score=self.benchmark_score,
        )

    @property
    def identifier(
        self,
    ) -> str:
        return (
            f"{self.model_name}:"
            f"{self.model_version}"
        )

    @property
    def has_uri(
        self,
    ) -> bool:
        return (
            self.model_uri
            is not None
        )

    @property
    def has_artifact(
        self,
    ) -> bool:
        return (
            self.artifact_path
            is not None
        )

    @property
    def has_tags(
        self,
    ) -> bool:
        return bool(
            self.tags,
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_development(
        self,
    ) -> bool:
        return (
            self.stage
            == ModelStage.DEVELOPMENT
        )

    @property
    def is_validation(
        self,
    ) -> bool:
        return (
            self.stage
            == ModelStage.VALIDATION
        )

    @property
    def is_staging(
        self,
    ) -> bool:
        return (
            self.stage
            == ModelStage.STAGING
        )

    @property
    def is_canary(
        self,
    ) -> bool:
        return (
            self.stage
            == ModelStage.CANARY
        )

    @property
    def is_production(
        self,
    ) -> bool:
        return (
            self.stage
            == ModelStage.PRODUCTION
        )

    @property
    def is_archived(
        self,
    ) -> bool:
        return (
            self.stage
            == ModelStage.ARCHIVED
        )

    @property
    def is_deployable(
        self,
    ) -> bool:
        return (
            self.stage
            in {
                ModelStage.CANARY,
                ModelStage.PRODUCTION,
            }
        )