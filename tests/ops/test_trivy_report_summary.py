"""Trivy evidence analysis must be deterministic and fail closed."""

from __future__ import annotations

import json

import pytest

from src.application.security.trivy_report import summarize_trivy_report
from src.infrastructure.operations.summarize_trivy_image_scan import main


def _payload() -> dict:
    return {
        "Results": [
            {
                "Target": "Debian OS",
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-2026-76642",
                        "PkgName": "bsdutils",
                        "Severity": "HIGH",
                        "FixedVersion": "",
                    },
                    {
                        "VulnerabilityID": "CVE-2026-76642",
                        "PkgName": "libblkid1",
                        "Severity": "HIGH",
                    },
                    {
                        "VulnerabilityID": "CVE-2026-85091",
                        "PkgName": "zlib1g",
                        "Severity": "HIGH",
                        "FixedVersion": "1:1.3.dfsg+really1.3.1-1+deb13u1",
                    },
                    {
                        "VulnerabilityID": "CVE-2023-45853",
                        "PkgName": "zlib1g",
                        "Severity": "CRITICAL",
                        "FixedVersion": None,
                    },
                    {
                        "VulnerabilityID": "CVE-0000-0000",
                        "Severity": "LOW",
                    },
                ],
            },
            {"Target": "Python packages", "Vulnerabilities": None},
        ]
    }


def test_counts_matches_but_deduplicates_advisory_identifiers() -> None:
    result = summarize_trivy_report(_payload())
    assert result.high == 3
    assert result.critical == 1
    assert result.total == 4
    assert result.distinct_advisories == 3
    assert result.with_fixed_version == 1
    assert result.without_fixed_version == 3
    assert result.blocked is True
    assert "HIGH package/advisory matches: **3**" in result.to_markdown()
    assert "with no fixed version stated by scanner: **3**" in result.to_markdown()


def test_valid_empty_scan_is_not_a_trivy_policy_bypass() -> None:
    result = summarize_trivy_report({"Results": []})
    assert result.total == 0
    assert result.distinct_advisories == 0
    assert result.blocked is False


@pytest.mark.parametrize(
    "invalid",
    [
        None,
        {},
        {"Results": None},
        {"Results": {}},
        {"Results": [{"Vulnerabilities": {}}]},
        {"Results": [None]},
        {
            "Results": [
                {"Vulnerabilities": [{"Severity": "HIGH"}]},
            ]
        },
    ],
)
def test_rejects_missing_and_malformed_evidence(invalid: object) -> None:
    with pytest.raises(ValueError, match="Invalid Trivy JSON"):
        summarize_trivy_report(invalid)


def test_cli_writes_exact_summary_to_job_file(tmp_path, monkeypatch) -> None:
    report = tmp_path / "trivy.json"
    report.write_text(json.dumps(_payload()), encoding="utf-8")
    output = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(output))
    monkeypatch.setattr(
        "sys.argv", ["summarize_trivy_image_scan", "--input", str(report)]
    )
    assert main() == 0
    contents = output.read_text(encoding="utf-8")
    assert "Distinct advisory identifiers: **3**" in contents
    assert "Release remains BLOCKED" in contents


def test_cli_rejects_invalid_json_without_fake_clean_summary(
    tmp_path, monkeypatch
) -> None:
    report = tmp_path / "trivy.json"
    report.write_text("not JSON", encoding="utf-8")
    output = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(output))
    monkeypatch.setattr(
        "sys.argv", ["summarize_trivy_image_scan", "--input", str(report)]
    )
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    assert not output.exists()
