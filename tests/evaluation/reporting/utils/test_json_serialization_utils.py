from __future__ import annotations

import json
from datetime import UTC, datetime

from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection
from src.evaluation.reporting.utils.json_serialization_utils import JSONSerializationUtils


def test_to_json_serializes_enums_and_datetime_with_trailing_newline() -> None:
    rendered = JSONSerializationUtils.to_json(
        payload={
            "trend": SummaryTrendDirection.IMPROVING,
            "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        },
    )

    assert rendered.endswith("\n")
    payload = json.loads(rendered)
    assert payload["trend"] == "improving"
    assert payload["created_at"] == "2026-01-01T00:00:00+00:00"
