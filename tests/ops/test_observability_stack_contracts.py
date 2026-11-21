"""Static invariants for the opt-in container-only observability stack."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")
BASE = Path("ops/observability")


def load(filename: str):
    return yaml.safe_load((BASE / filename).read_text(encoding="utf-8"))


def test_private_network_no_public_metrics() -> None:
    doc = load("compose.yml")
    svc = doc["services"]
    assert set(svc) == {
        "tempo", "otel-collector", "prometheus", "alertmanager", "grafana"
    }
    assert doc["networks"]["telemetry-private"]["internal"] is True
    assert svc["grafana"]["ports"] == ["127.0.0.1:3000:3000"]
    for name, item in svc.items():
        assert name == "grafana" or not item.get("ports")
        assert "telemetry-private" in item["networks"]
        assert item["cap_drop"] == ["ALL"]
        assert item["security_opt"] == ["no-new-privileges:true"]
    assert svc["alertmanager"]["networks"] == [
        "telemetry-private", "notifications-egress"
    ]
    assert all(
        "notifications-egress" not in item["networks"]
        for name, item in svc.items() if name != "alertmanager"
    )


def test_secrets_required_and_authenticated_grafana() -> None:
    doc = load("compose.yml")
    assert "GRAFANA_ADMIN_PASSWORD_FILE" in doc["secrets"][
        "grafana_admin_password"
    ]["file"]
    assert "ALERT_WEBHOOK_URL_FILE" in doc["secrets"][
        "alert_webhook_url"
    ]["file"]
    env = doc["services"]["grafana"]["environment"]
    assert env["GF_AUTH_ANONYMOUS_ENABLED"] == "false"
    assert env["GF_SECURITY_ADMIN_PASSWORD__FILE"] == (
        "/run/secrets/grafana_admin_password"
    )
    assert "alert_webhook_url" in doc["services"]["alertmanager"]["secrets"]
    assert "url_file: /run/secrets/alert_webhook_url" in (
        BASE / "alertmanager.yml"
    ).read_text(encoding="utf-8")


def test_collector_pipelines_and_prometheus_target() -> None:
    collector = load("collector.yml")
    pipe = collector["service"]["pipelines"]
    assert set(pipe) == {"metrics", "traces"}
    assert pipe["metrics"]["exporters"] == ["prometheus"]
    assert pipe["traces"]["exporters"] == ["otlp/tempo"]
    assert collector["processors"]["memory_limiter"]["limit_mib"] > 0
    assert collector["exporters"]["prometheus"]["endpoint"] == (
        "0.0.0.0:9464"
    )
    prometheus = load("prometheus.yml")
    assert prometheus["scrape_configs"][0]["static_configs"][0][
        "targets"
    ] == ["otel-collector:9464"]
    assert prometheus["rule_files"] == ["/etc/prometheus/slo-rules.yml"]
    assert prometheus["alerting"]["alertmanagers"][0]["static_configs"][0][
        "targets"
    ] == ["alertmanager:9093"]


def test_grafana_provisioning_matches_dashboard() -> None:
    src = load("grafana/provisioning/datasources/datasources.yml")
    dash = load("grafana/provisioning/dashboards/dashboards.yml")
    assert {s["uid"] for s in src["datasources"]} == {
        "prometheus", "tempo"
    }
    assert dash["providers"][0]["options"]["path"] == (
        "/var/lib/grafana/dashboards"
    )
    dashboard = json.loads(
        (BASE / "grafana/ai-interview-http-dataset-dashboard.json").read_text(
            encoding="utf-8"
        )
    )
    assert dashboard["__inputs"] == []
    assert len(dashboard["panels"]) == 8
    assert all(
        panel["datasource"]["uid"] == "prometheus"
        for panel in dashboard["panels"]
    )
    assert all(
        target["datasource"]["uid"] == "prometheus"
        for panel in dashboard["panels"]
        for target in panel["targets"]
    )
    exprs = " ".join(
        target["expr"] for panel in dashboard["panels"]
        for target in panel["targets"]
    )
    assert "interview:http_5xx:ratio_30d" in exprs


def test_multiwindow_error_budget_and_min_traffic_guards() -> None:
    rules = load("slo-rules.yml")["groups"][0]["rules"]
    alerts = {r["alert"]: r for r in rules if "alert" in r}
    assert set(alerts) == {
        "InterviewAPIAvailabilityFastBurn",
        "InterviewAPIAvailabilitySlowBurn",
        "InterviewAPIExporterMissing",
    }
    fast = alerts["InterviewAPIAvailabilityFastBurn"]["expr"]
    slow = alerts["InterviewAPIAvailabilitySlowBurn"]["expr"]
    for fragment in ("14.4 * 0.001", "ratio_1h", "ratio_5m",
                     ">= 100", ">= 10"):
        assert fragment in fast
    for fragment in ("6 * 0.001", "ratio_6h", "ratio_30m",
                     ">= 300", ">= 30"):
        assert fragment in slow
    assert all(
        r["labels"]["severity"] in {"critical", "warning"}
        for r in alerts.values()
    )
