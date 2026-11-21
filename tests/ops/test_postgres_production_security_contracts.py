"""Validation of opt-in Kubernetes protection and monitoring manifests."""

from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")
ROOT = Path("ops/postgres-ha")


def load(path: str) -> dict:
    data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_network_policy_limits_cluster_ingress_only() -> None:
    doc = load("security/network-policy.yaml")
    assert doc["kind"] == "NetworkPolicy"
    assert doc["metadata"]["namespace"] == "interview-db"
    spec = doc["spec"]
    assert spec["podSelector"]["matchLabels"] == {
        "cnpg.io/cluster": "interview-db-primary"
    }
    assert spec["policyTypes"] == ["Ingress"]
    assert len(spec["ingress"]) == 4
    assert {row["ports"][0]["port"] for row in spec["ingress"]} == {
        5432, 8000, 9187
    }
    assert all(row.get("from") for row in spec["ingress"])


def test_status_port_exclusive_to_operator_namespace() -> None:
    spec = load("security/network-policy.yaml")["spec"]
    status = [
        row for row in spec["ingress"]
        if row["ports"][0]["port"] == 8000
    ]
    assert len(status) == 1
    assert status[0]["from"] == [{
        "namespaceSelector": {
            "matchLabels": {"kubernetes.io/metadata.name": "cnpg-system"}
        }
    }]


def test_readiness_auditor_has_no_write_or_secrets_rights() -> None:
    text = (ROOT / "security/read-only-rbac.yaml").read_text()
    sa, role, binding = list(yaml.safe_load_all(text))
    assert sa["automountServiceAccountToken"] is False
    assert role["kind"] == "Role"
    assert binding["kind"] == "RoleBinding"
    assert binding["roleRef"]["name"] == role["metadata"]["name"]
    assert all(
        set(item["verbs"]) <= {"get", "list", "watch"}
        and "secrets" not in item["resources"]
        for item in role["rules"]
    )


def test_external_secrets_require_approved_references() -> None:
    names = (
        ("security/backup-writer-external-secret.yaml", "interview-db-s3-writer"),
        (
            "security/restore-reader-external-secret.yaml",
            "interview-db-s3-restore-reader",
        ),
    )
    for path, expected in names:
        doc = load(path)
        assert doc["apiVersion"] == "external-secrets.io/v1"
        assert doc["kind"] == "ExternalSecret"
        spec = doc["spec"]
        assert spec["target"]["name"] == expected
        assert spec["target"]["deletionPolicy"] == "Retain"
        assert spec["secretStoreRef"]["name"].startswith("REPLACE_WITH_")
        assert {row["secretKey"] for row in spec["data"]} == {
            "ACCESS_KEY_ID", "ACCESS_SECRET_KEY"
        }
        assert all(
            row["remoteRef"]["key"].startswith("REPLACE_WITH_")
            for row in spec["data"]
        )
    assert load("kubernetes/object-store.yaml")["spec"][
        "configuration"
    ]["s3Credentials"]["accessKeyId"]["name"] == names[0][1]
    assert load("recovery/source-object-store.yaml")["spec"][
        "configuration"
    ]["s3Credentials"]["accessKeyId"]["name"] == names[1][1]


def test_plugin_metric_alerts_are_bounded_and_have_missing_data_signal() -> None:
    data = load("monitoring/postgres-recovery-alerts.yml")
    alerts = {x["alert"]: x for x in data["groups"][0]["rules"]}
    assert len(alerts) == 5
    assert "InterviewPostgresBackupStale" in alerts
    assert "InterviewPostgresBackupMetricMissing" in alerts
    assert "InterviewPostgresReplicationMetricMissing" in alerts
    assert "InterviewPostgresInsufficientStreamingReplicas" in alerts
    text = (ROOT / "monitoring/postgres-recovery-alerts.yml").read_text()
    assert "barman_cloud_cloudnative_pg_io_last_available_backup_timestamp" in text
    assert "barman_cloud_cloudnative_pg_io_last_failed_backup_timestamp" in text
    assert "cnpg_pg_replication_streaming_replicas" in text
    assert all(
        row["labels"]["service"] == "interview-db"
        and row["labels"]["severity"] in {"critical", "warning"}
        for row in alerts.values()
    )
