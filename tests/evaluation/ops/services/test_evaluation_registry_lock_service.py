from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.services.evaluation_registry_lock_service import (
    EvaluationRegistryLockService,
)
from tests.evaluation.ops.factories import evaluation_registry


def test_evaluation_registry_lock_service_should_lock_and_unlock_registry() -> None:
    registry = evaluation_registry(is_locked=False)

    locked = EvaluationRegistryLockService.lock(registry=registry)
    unlocked = EvaluationRegistryLockService.unlock(registry=locked)

    assert locked.is_locked is True
    assert locked.updated_at is not None
    assert unlocked.is_locked is False
    assert unlocked.updated_at is not None


def test_evaluation_registry_lock_service_should_return_same_registry_when_idempotent() -> None:
    locked = evaluation_registry(is_locked=True)
    unlocked = evaluation_registry(is_locked=False)

    assert EvaluationRegistryLockService.lock(registry=locked) is locked
    assert EvaluationRegistryLockService.unlock(registry=unlocked) is unlocked


def test_evaluation_registry_lock_service_should_raise_when_locked() -> None:
    with pytest.raises(EvaluationValidationError, match="registry is locked"):
        EvaluationRegistryLockService.ensure_unlocked(
            registry=evaluation_registry(is_locked=True),
        )
