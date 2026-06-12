from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.benchmark_history_validator import (
    BenchmarkHistoryValidator,
)
from tests.evaluation.ops.factories import history_entry


def test_benchmark_history_validator_should_accept_valid_payload() -> None:
    BenchmarkHistoryValidator.validate(
        history_id="history-1",
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        entries=(history_entry(),),
        created_at=datetime.now(tz=timezone.utc),
        notes="Valid history.",
    )


def test_benchmark_history_validator_should_reject_mismatched_entry_version() -> None:
    with pytest.raises(EvaluationValidationError, match="benchmark_version does not match"):
        BenchmarkHistoryValidator.validate(
            history_id="history-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            entries=(history_entry(benchmark_version="2.0.0"),),
            created_at=datetime.now(tz=timezone.utc),
        )


def test_benchmark_history_validator_should_reject_invalid_updated_at_type() -> None:
    with pytest.raises(EvaluationValidationError, match="updated_at must be datetime"):
        BenchmarkHistoryValidator.validate(
            history_id="history-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            entries=(),
            created_at=datetime.now(tz=timezone.utc),
            updated_at="2026-01-01",  # type: ignore[arg-type]
        )


def test_benchmark_history_validator_should_reject_updated_at_before_created_at() -> None:
    created_at = datetime.now(tz=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="earlier than created_at"):
        BenchmarkHistoryValidator.validate(
            history_id="history-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            entries=(),
            created_at=created_at,
            updated_at=created_at - timedelta(seconds=1),
        )
