"""Black-box CLI exit codes and privacy guarantees for DR evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

def evidence() -> dict:
    return {
        "observed_at": "2026-11-22T12:00:00Z",
        "instances_desired": 3,
        "instances_ready": 3,
        "primary_known": True,
        "last_successful_backup_at": "2026-11-22T02:00:00Z",
        "last_archived_wal_at": "2026-11-22T11:55:00Z",
        "restore_drill": {
            "independently_verified": True,
            "incident_declared_at": "2026-11-22T11:20:00Z",
            "service_writable_at": "2026-11-22T11:25:00Z",
            "latest_committed_at": "2026-11-22T11:19:00Z",
            "latest_recovered_commit_at": "2026-11-22T11:18:00Z",
        },
    }



def run_cli(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable, "-m",
            "src.infrastructure.operations.dr_readiness_cli",
            "--evidence", str(path), *args,
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )


def test_valid_evidence_emits_machine_readable_success(tmp_path: Path) -> None:
    path = tmp_path / "dr.json"
    path.write_text(json.dumps(evidence()), encoding="utf-8")
    result = run_cli(path)
    assert result.returncode == 0
    assert json.loads(result.stdout)["ready"] is True
    assert "rto" in json.loads(result.stdout)["observed_metrics_seconds"]


def test_valid_but_unhealthy_evidence_blocks_rollout(tmp_path: Path) -> None:
    path = tmp_path / "dr.json"
    data = evidence()
    data["restore_drill"]["independently_verified"] = False
    path.write_text(json.dumps(data), encoding="utf-8")
    result = run_cli(path)
    assert result.returncode == 1
    assert json.loads(result.stdout)["ready"] is False


def test_invalid_input_is_private_and_returns_exit_two(tmp_path: Path) -> None:
    path = tmp_path / "SECRET-NAME.json"
    path.write_text('{"password": "SECRET-DATA"}', encoding="utf-8")
    result = run_cli(path)
    assert result.returncode == 2
    assert json.loads(result.stdout)["ready"] is False
    assert "SECRET" not in result.stdout + result.stderr
