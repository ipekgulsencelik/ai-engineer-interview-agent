"""Grafana dashboard contract: valid JSON and linked metrics."""

from __future__ import annotations

import json
from pathlib import Path


def test_dashboard_is_importable_and_uses_expected_promql_metrics() -> None:
    dashboard = json.loads(
        Path(
            "ops/observability/grafana/ai-interview-http-dataset-dashboard.json"
        ).read_text(encoding="utf-8")
    )
    assert dashboard["uid"] == "ai-interview-api-ops"
    assert dashboard["schemaVersion"] >= 39
    assert len(dashboard["panels"]) >= 6
    ids = [panel["id"] for panel in dashboard["panels"]]
    assert len(ids) == len(set(ids))
    promql = " ".join(
        target["expr"]
        for panel in dashboard["panels"]
        for target in panel["targets"]
    )
    assert "http_server_requests_total" in promql
    assert "http_server_request_duration_seconds_bucket" in promql
    assert "dataset_operations_total" in promql
    assert "histogram_quantile" in promql
    assert "status_class" in promql
    assert "candidate_answer" not in promql
    assert "raw_path" not in promql
    assert all(
        panel["datasource"]["uid"] == "${DS_PROMETHEUS}"
        for panel in dashboard["panels"]
    )


def test_http_alert_examples_reference_exported_instruments() -> None:
    rules = Path(
        "ops/observability/prometheus-rules-example.yml"
    ).read_text(encoding="utf-8")
    assert "InterviewAPIHigh5xxRatio" in rules
    assert "InterviewAPIHighP95Latency" in rules
    assert "http_server_requests_total" in rules
    assert "http_server_request_duration_seconds_bucket" in rules
