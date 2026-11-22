"""Pure JUnit evidence evaluation for mandatory live integrations."""

from __future__ import annotations

from dataclasses import dataclass
from xml.etree import ElementTree


@dataclass(frozen=True, slots=True)
class IntegrationCoverageResult:
    """Counts collected cases, including cases not actually executed."""

    collected: int
    skipped: int
    failures: int
    errors: int

    @property
    def valid(self) -> bool:
        return (
            self.collected > 0
            and self.skipped == 0
            and self.failures == 0
            and self.errors == 0
        )


def _count(suite: ElementTree.Element, key: str) -> int:
    raw = suite.get(key)
    try:
        count = int(raw) if raw is not None else -1
    except ValueError as exc:
        raise ValueError(f"Invalid JUnit evidence: {key} is not an integer") from exc
    if count < 0:
        raise ValueError(f"Invalid JUnit evidence: {key} is missing/negative")
    return count


def summarize_integration_junit(xml: str) -> IntegrationCoverageResult:
    """Reject missing, malformed and contradictory JUnit XML, never silently skip."""
    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError as exc:
        raise ValueError("Invalid JUnit evidence: malformed XML") from exc

    if root.tag == "testsuite":
        suites = [root]
    elif root.tag == "testsuites":
        suites = list(root)
    else:
        raise ValueError("Invalid JUnit evidence: unexpected root")

    if not suites or any(suite.tag != "testsuite" for suite in suites):
        raise ValueError("Invalid JUnit evidence: missing testsuites")

    totals = [0, 0, 0, 0]
    for suite in suites:
        cases = list(suite.iter("testcase"))
        collected = _count(suite, "tests")
        skipped = sum(case.find("skipped") is not None for case in cases)
        failures = sum(case.find("failure") is not None for case in cases)
        errors = sum(case.find("error") is not None for case in cases)

        if (
            len(cases) != collected
            or skipped != _count(suite, "skipped")
            or failures != _count(suite, "failures")
            or errors != _count(suite, "errors")
        ):
            raise ValueError("Invalid JUnit evidence: inconsistent suite counts")

        for case in cases:
            outcomes = (
                (case.find("skipped") is not None)
                + (case.find("failure") is not None)
                + (case.find("error") is not None)
            )
            if outcomes > 1:
                raise ValueError("Invalid JUnit evidence: contradictory case")

        totals[0] += collected
        totals[1] += skipped
        totals[2] += failures
        totals[3] += errors

    return IntegrationCoverageResult(
        collected=totals[0],
        skipped=totals[1],
        failures=totals[2],
        errors=totals[3],
    )
