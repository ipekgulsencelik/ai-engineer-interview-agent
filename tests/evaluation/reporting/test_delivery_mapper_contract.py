"""Real delivery mapping invariants: no lost fields or metadata aliasing."""

from __future__ import annotations

from datetime import UTC, datetime

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
