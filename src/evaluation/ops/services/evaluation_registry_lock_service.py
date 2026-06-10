from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.evaluation_registry import (
    EvaluationRegistry,
)


class EvaluationRegistryLockService:
    """
    Lock service for immutable evaluation registry snapshots.
    """

    @staticmethod
    def ensure_unlocked(
        *,
        registry: EvaluationRegistry,
    ) -> None:
        if registry.is_locked:
            raise EvaluationValidationError(
                "registry is locked."
            )

    @staticmethod
    def lock(
        *,
        registry: EvaluationRegistry,
    ) -> EvaluationRegistry:
        if registry.is_locked:
            return registry

        return replace(
            registry,
            is_locked=True,
            updated_at=datetime.now(tz=timezone.utc),
        )

    @staticmethod
    def unlock(
        *,
        registry: EvaluationRegistry,
    ) -> EvaluationRegistry:
        if not registry.is_locked:
            return registry

        return replace(
            registry,
            is_locked=False,
            updated_at=datetime.now(tz=timezone.utc),
        )