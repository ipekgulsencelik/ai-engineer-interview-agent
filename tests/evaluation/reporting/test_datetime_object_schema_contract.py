"""Real datetime objects must satisfy reporting schemas and artifact factories."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.domain.validation.schema_validator import SchemaValidator
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.factories.report_artifact_factory import (
    ReportArtifactFactory,
)
from src.evaluation.reporting.resolvers.content_type_resolver import (
    ContentTypeResolver,
)
from src.evaluation.reporting.schemas.bi_dataset_schema import BI_DATASET_SCHEMA
from src.evaluation.reporting.schemas.report_artifact_schema import (
    REPORT_ARTIFACT_SCHEMA,
)
from src.evaluation.reporting.schemas.report_permission_schema import (
    REPORT_PERMISSION_SCHEMA,
)
from src.evaluation.reporting.schemas.report_template_schema import (
    REPORT_TEMPLATE_SCHEMA,
)
from src.evaluation.reporting.schemas.stream_event_schema import (
    STREAM_EVENT_SCHEMA,
)
from src.evaluation.reporting.schemas.telemetry_metric_schema import (
    TELEMETRY_METRIC_SCHEMA,
)


@pytest.mark.parametrize(
    ("schema", "field"),
    [
        (BI_DATASET_SCHEMA, "created_at"),
        (REPORT_ARTIFACT_SCHEMA, "created_at"),
        (REPORT_PERMISSION_SCHEMA, "created_at"),
        (REPORT_TEMPLATE_SCHEMA, "created_at"),
        (STREAM_EVENT_SCHEMA, "occurred_at"),
        (TELEMETRY_METRIC_SCHEMA, "recorded_at"),
    ],
)
def test_reporting_timestamp_schema_accepts_datetime_not_string(
    schema: dict[str, object], field: str
) -> None:
    single = {field: schema[field]}
    SchemaValidator.validate(
        values={field: datetime(2026, 11, 23, tzinfo=UTC)},
        schema=single,
        error_factory=EvaluationValidationError,
    )
    with pytest.raises(EvaluationValidationError):
        SchemaValidator.validate(
            values={field: "2026-11-23T00:00:00+00:00"},
            schema=single,
            error_factory=EvaluationValidationError,
        )


def test_optional_permission_expiry_accepts_none_and_datetime() -> None:
    rule = {"expires_at": REPORT_PERMISSION_SCHEMA["expires_at"]}
    for expiry in (None, datetime(2027, 1, 1, tzinfo=UTC)):
        SchemaValidator.validate(values={"expires_at": expiry}, schema=rule)


def test_real_artifact_factory_constructs_datetime_valued_report(tmp_path) -> None:
    artifact = ReportArtifactFactory(
        content_type_resolver=ContentTypeResolver(),
    ).create(
        title="Weekly Report",
        report_type="executive_summary",
        run_id="run-01",
        experiment_id="experiment-01",
        report_format="json",
        output_path=tmp_path / "summary.json",
        content="{}",
    )
    assert artifact.created_at.tzinfo is not None
    assert artifact.format == "json"
    assert artifact.content_type == "application/json"
