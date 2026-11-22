"""Ensure CI never silently marks skipped real integrations as green."""

from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")


def test_required_integration_jobs_reject_skips_and_archive_junit() -> None:
    workflow = yaml.safe_load(
        Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    )
    jobs = workflow["jobs"]
    for job, filename in (
        ("postgres-integration", "postgres-integration.xml"),
        ("telemetry-sdk", "telemetry-integration.xml"),
    ):
        steps = jobs[job]["steps"]
        run_tests = next(
            step for step in steps
            if "python -m pytest" in step.get("run", "")
        )
        assert "--junitxml=" + filename in run_tests["run"]
        assert " -rs" in run_tests["run"]
        enforce = next(
            step for step in steps
            if "verify_integration_test_coverage" in step.get("run", "")
        )
        assert enforce["if"] == "always()"
        assert "--report " + filename in enforce["run"]
        assert "continue-on-error" not in enforce
        archive = next(
            step for step in steps
            if step.get("name", "").startswith("Archive ")
        )
        assert archive["if"] == "always()"
        assert archive["with"]["path"] == filename
        assert archive["with"]["if-no-files-found"] == "error"
        assert archive["with"]["retention-days"] == 14
        assert archive["uses"].startswith("actions/upload-artifact@")
    base = jobs["quality-gates"]["steps"]
    assert any(step.get("run") == "uv run pytest -q -rs" for step in base)
