"""Live integration JUnit policy must reject false-positive CI success."""

from __future__ import annotations

import pytest

from src.application.quality.integration_test_coverage import (
    summarize_integration_junit,
)
from src.infrastructure.operations.verify_integration_test_coverage import main


def _report(*, skipped: int = 0, failures: int = 0) -> str:
    cases = [
        '<testcase classname="live" name="one"/>',
    ]
    if skipped:
        cases.append(
            '<testcase classname="live" name="two">'
            '<skipped message="missing environment"/></testcase>'
        )
    if failures:
        cases.append(
            '<testcase classname="live" name="three">'
            '<failure message="broken"/></testcase>'
        )
    return (
        '<testsuites><testsuite name="pytest" '
        f'tests="{len(cases)}" failures="{failures}" '
        f'errors="0" skipped="{skipped}">'
        + "".join(cases)
        + "</testsuite></testsuites>"
    )


def test_executed_cases_pass_without_any_skips() -> None:
    result = summarize_integration_junit(_report())
    assert (result.collected, result.skipped) == (1, 0)
    assert result.valid


@pytest.mark.parametrize(
    "xml",
    [
        "",
        "<testsuites>",
        "<unexpected/>",
        "<testsuites/>",
        '<testsuite tests="0" failures="0" errors="0" skipped="0"/>',
        '<testsuite tests="1" failures="0" errors="0" skipped="0"/>',
        '<testsuite tests="bad" failures="0" errors="0" skipped="0"/>',
        '<testsuite tests="1" failures="0" errors="0" skipped="1">'
        '<testcase name="actual"/></testsuite>',
        '<testsuite tests="1" failures="0" errors="0" skipped="0">'
        '<testcase name="one"><skipped/></testcase></testsuite>',
    ],
)
def test_invalid_or_inconsistent_evidence_is_rejected(xml: str) -> None:
    if xml.startswith('<testsuite tests="0"'):
        assert not summarize_integration_junit(xml).valid
    else:
        with pytest.raises(ValueError, match="Invalid JUnit evidence"):
            summarize_integration_junit(xml)


def test_skip_and_failure_never_count_as_executed_success() -> None:
    skipped = summarize_integration_junit(_report(skipped=1))
    assert skipped.skipped == 1
    assert not skipped.valid
    failed = summarize_integration_junit(_report(failures=1))
    assert failed.failures == 1
    assert not failed.valid


def test_cli_fails_closed_on_missing_report(tmp_path) -> None:
    assert main(["--report", str(tmp_path / "absent.xml")]) == 1


def test_cli_requires_all_real_cases_to_execute(tmp_path) -> None:
    path = tmp_path / "integration.xml"
    path.write_text(_report(skipped=1), encoding="utf-8")
    assert main(["--report", str(path)]) == 1
    path.write_text(_report(), encoding="utf-8")
    assert main(["--report", str(path)]) == 0
