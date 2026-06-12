from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.evaluation_registry_validator import (
    EvaluationRegistryValidator,
)
from tests.evaluation.ops.factories import registered_benchmark


def test_evaluation_registry_validator_should_accept_valid_payload() -> None:
    EvaluationRegistryValidator.validate(
        registry_id="registry-1",
        registry_name="Evaluation Registry",
        version="1.0.0",
        benchmarks=(registered_benchmark(),),
        created_at=datetime.now(tz=timezone.utc),
        is_locked=False,
        notes="Valid registry.",
    )


def test_evaluation_registry_validator_should_reject_duplicate_benchmark_keys() -> None:
    benchmark = registered_benchmark()

    with pytest.raises(EvaluationValidationError, match="duplicate identity"):
        EvaluationRegistryValidator.validate(
            registry_id="registry-1",
            registry_name="Evaluation Registry",
            version="1.0.0",
            benchmarks=(benchmark, benchmark),
            created_at=datetime.now(tz=timezone.utc),
            is_locked=False,
        )


def test_evaluation_registry_validator_should_reject_invalid_timestamps() -> None:
    created_at = datetime.now(tz=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="earlier than created_at"):
        EvaluationRegistryValidator.validate(
            registry_id="registry-1",
            registry_name="Evaluation Registry",
            version="1.0.0",
            benchmarks=(),
            created_at=created_at,
            updated_at=created_at - timedelta(seconds=1),
            is_locked=False,
        )
