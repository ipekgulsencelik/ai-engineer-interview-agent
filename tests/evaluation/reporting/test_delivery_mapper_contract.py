"""Real delivery mapping invariants: no lost fields or metadata aliasing."""

from __future__ import annotations

from datetime import UTC, datetime
from dataclasses import replace
from typing import cast

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)
from src.evaluation.reporting.mappers.report_delivery_result_mapper import (
    ReportDeliveryResultMapper,
)
from src.evaluation.reporting.schemas.report_delivery_result_schema import (
    ReportDeliveryResultSchema,
)


def _valid_delivery() -> ReportDeliveryResult:
    return ReportDeliveryResult(
        delivery_id="delivery-001",
        report_id="report-001",
        artifact_id="artifact-001",
        delivery_type="email",
        destination="reports@example.invalid",
        success=True,
        delivered_at=datetime(2026, 11, 22, tzinfo=UTC),
        provider="smtp",
        status_code=202,
        retry_count=2,
        metadata={"classification": "internal"},
    )


def test_mapping_preserves_all_fields_with_independent_metadata() -> None:
    original = _valid_delivery()
    schema = ReportDeliveryResultMapper.to_schema(original)
    assert isinstance(schema, ReportDeliveryResultSchema)
    assert schema.artifact_id == original.artifact_id
    assert schema.provider == original.provider
    assert schema.status_code == original.status_code
    assert schema.retry_count == original.retry_count
    assert schema.metadata == original.metadata
    assert schema.metadata is not original.metadata

    restored = ReportDeliveryResultMapper.from_schema(schema)
    assert restored == original
    assert restored.metadata is not schema.metadata
    assert restored.metadata is not original.metadata


def test_failure_metadata_roundtrips_without_losing_error() -> None:
    failed = ReportDeliveryResult(
        delivery_id="failed-001",
        report_id="report-001",
        artifact_id="artifact-001",
        delivery_type="webhook",
        destination="https://example.invalid/events",
        success=False,
        delivered_at=datetime(2026, 11, 22, tzinfo=UTC),
        status_code=503,
        error_message="Service unavailable",
        retry_count=3,
    )
    assert ReportDeliveryResultMapper.from_schema(
        ReportDeliveryResultMapper.to_schema(failed)
    ) == failed


def test_schema_rejects_missing_required_artifact_id() -> None:
    with pytest.raises(EvaluationValidationError):
        ReportDeliveryResultSchema(
            delivery_id="delivery-001",
            report_id="report-001",
            artifact_id="",
            delivery_type="email",
            destination="reports@example.invalid",
            success=True,
            delivered_at=datetime(2026, 11, 22, tzinfo=UTC),
        )


@pytest.mark.parametrize("invalid_type", ["unknown", "", "not-a-channel"])
def test_delivery_dto_rejects_unsupported_type(invalid_type: str) -> None:
    schema = ReportDeliveryResultMapper.to_schema(_valid_delivery())
    with pytest.raises(EvaluationValidationError):
        replace(schema, delivery_type=invalid_type)


def test_failed_delivery_dto_requires_error_and_success_disallows_error() -> None:
    schema = ReportDeliveryResultMapper.to_schema(_valid_delivery())
    with pytest.raises(EvaluationValidationError, match="error_message"):
        replace(schema, success=False, error_message=None)
    with pytest.raises(EvaluationValidationError, match="error_message"):
        replace(schema, success=True, error_message="unexpected")
    with pytest.raises(EvaluationValidationError, match="status_code"):
        replace(schema, status_code=99)


@pytest.mark.parametrize(
    "invalid_metadata",
    [[], 0, False, {"": "value"}, {"key": 1}],
)
def test_delivery_dto_rejects_malformed_metadata(invalid_metadata: object) -> None:
    schema = ReportDeliveryResultMapper.to_schema(_valid_delivery())
    with pytest.raises(EvaluationValidationError):
        replace(
            schema,
            metadata=cast(dict[str, str] | None, invalid_metadata),
        )
