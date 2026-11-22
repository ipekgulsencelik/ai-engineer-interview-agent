"""Static safety and compatibility contracts for the PostgreSQL HA/DR manifests."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

BASE = Path("ops/postgres-ha")
PLUGIN = "barman-cloud.cloudnative-pg.io"


def load(name: str) -> dict:
    return yaml.safe_load((BASE / name).read_text(encoding="utf-8"))


def test_ha_cluster_requires_three_instances_and_zone_spread() -> None:
    cluster = load("kubernetes/cluster.yaml")
    spec = cluster["spec"]
    assert cluster["metadata"]["namespace"] == "interview-db"
    assert spec["instances"] == 3
    assert spec["minSyncReplicas"] == 1
    assert spec["maxSyncReplicas"] == 1
    assert spec["affinity"]["podAntiAffinityType"] == "required"
    assert spec["affinity"]["topologyKey"] == "topology.kubernetes.io/zone"
    assert spec["primaryUpdateStrategy"] == "supervised"
    assert spec["imageName"].startswith(
        "ghcr.io/cloudnative-pg/postgresql:16.16-"
    )
    assert spec["plugins"] == [{
        "name": PLUGIN,
        "isWALArchiver": True,
        "parameters": {"barmanObjectName": "interview-db-primary-backups"},
    }]


def test_backups_are_plugin_scheduled_and_initial_backup_immediate() -> None:
    store = load("kubernetes/object-store.yaml")
    config = store["spec"]["configuration"]
    assert store["kind"] == "ObjectStore"
    assert store["apiVersion"] == "barmancloud.cnpg.io/v1"
    assert config["destinationPath"].startswith("s3://REPLACE_WITH_REAL")
    assert "endpointURL" not in config  # use cloud provider TLS defaults
    assert store["spec"]["retentionPolicy"] == "30d"
    assert config["wal"]["compression"] == "gzip"
    assert config["s3Credentials"]["accessKeyId"]["name"] == (
        "interview-db-s3-writer"
    )
    schedule = load("kubernetes/scheduled-backup.yaml")["spec"]
    assert schedule["immediate"] is True
    assert schedule["schedule"] == "0 0 2 * * *"
    assert len(schedule["schedule"].split()) == 6
    assert schedule["method"] == "plugin"
    assert schedule["pluginConfiguration"]["name"] == PLUGIN
    assert schedule["cluster"]["name"] == "interview-db-primary"


def test_pitr_never_overwrites_source_cluster_or_archive() -> None:
    source = load("recovery/source-object-store.yaml")
    recovered = load("recovery/pitr-cluster.yaml")
    c = recovered["spec"]
    assert recovered["metadata"]["namespace"] == "interview-db-restore"
    assert recovered["metadata"]["name"] != "interview-db-primary"
    assert c["instances"] == 1
    assert c["bootstrap"]["recovery"]["source"] == "source"
    assert c["bootstrap"]["recovery"]["recoveryTarget"]["targetTime"] == (
        "REPLACE_WITH_VERIFIED_UTC_TIMESTAMP"
    )
    assert c["externalClusters"][0]["plugin"]["parameters"] == {
        "barmanObjectName": "interview-db-backup-source",
        "serverName": "interview-db-primary",
    }
    assert "plugins" not in c  # no WAL archiving to source bucket
    assert source["spec"]["configuration"]["s3Credentials"][
        "accessKeyId"
    ]["name"] == "interview-db-s3-restore-reader"
    assert source["spec"]["configuration"]["destinationPath"] == load(
        "kubernetes/object-store.yaml"
    )["spec"]["configuration"]["destinationPath"]


def test_namespaces_are_separate_and_restricted() -> None:
    for path, expected in (
        ("kubernetes/namespace.yaml", "interview-db"),
        ("recovery/recovery-namespace.yaml", "interview-db-restore"),
    ):
        namespace = load(path)
        assert namespace["metadata"]["name"] == expected
        assert namespace["metadata"]["labels"][
            "pod-security.kubernetes.io/enforce"
        ] == "restricted"


def test_manifest_source_has_no_inline_secret_values() -> None:
    for path in sorted(BASE.glob("**/*.yaml")):
        text = path.read_text(encoding="utf-8")
        assert "kind: Secret" not in text
        assert "password:" not in text.lower()
        assert "secretaccesskey:" in text.lower() or (
            path.name not in ("object-store.yaml", "source-object-store.yaml")
        )


def test_real_pitr_drill_is_syntax_checked() -> None:
    script = BASE / "tests/pitr_docker_drill.sh"
    result = subprocess.run(
        ["bash", "-n", "-"],
        input=script.read_text(encoding="utf-8"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    text = script.read_text(encoding="utf-8")
    assert "pg_verifybackup" in text
    assert "pg_create_restore_point" in text
    assert "recovery.signal" in text
    assert "recovery_target_name" in text
    assert "pg_is_in_recovery" in text
    assert "1,2" in text and "3" in text
    assert "postgres:16.16" in text
    assert "POSTGRES_TEST_DSN" not in text  # disposable only
