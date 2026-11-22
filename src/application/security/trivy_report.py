"""Pure, fail-closed analysis of Trivy HIGH/CRITICAL image scan evidence.

A fixed version mentioned in a scanner report is a remediation *candidate*,
not proof that updating the package makes the entire container safe.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class TrivyFindingSummary:
    """Immutable counts of OS and library advisory-package matches."""

    high: int
    critical: int
    distinct_advisories: int
    with_fixed_version: int
    without_fixed_version: int

    @property
    def total(self) -> int:
        return self.high + self.critical

    @property
    def blocked(self) -> bool:
        return self.total > 0

    def to_markdown(self) -> str:
        """Readable evidence; this output never changes scan acceptance policy."""
        lines = [
            "### Production image Trivy findings (blocking)",
            "",
            f"- HIGH package/advisory matches: **{self.high}**",
            f"- CRITICAL package/advisory matches: **{self.critical}**",
            f"- Distinct advisory identifiers: **{self.distinct_advisories}**",
            (
                "- Findings with an explicit fixed package version: "
                f"**{self.with_fixed_version}**"
            ),
            (
                "- Findings with no fixed version stated by scanner: "
                f"**{self.without_fixed_version}**"
            ),
            "",
            (
                "**Release remains BLOCKED by the strict scan.**"
                if self.blocked
                else "No HIGH/CRITICAL findings reported in this scan."
            ),
            (
                "Fix-version metadata is advisory; a clean full-image Trivy "
                "gate and independent review remain mandatory."
            ),
            "",
        ]
        return "\n".join(lines)


def _as_mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"Invalid Trivy JSON: {name} must be an object")
    return value


def summarize_trivy_report(payload: object) -> TrivyFindingSummary:
    """Count advisory *matches*, unique IDs and candidate vendor fixes.

    A malformed/partial JSON report is an error, not an empty clean scan.
    """
    report = _as_mapping(payload, "root")
    if "Results" not in report:
        raise ValueError("Invalid Trivy JSON: missing Results")
    results = report["Results"]
    if not isinstance(results, list):
        raise ValueError("Invalid Trivy JSON: Results must be an array")

    high = critical = with_fix = without_fix = 0
    identifiers: set[str] = set()
    for entry in results:
        item = _as_mapping(entry, "Results entry")
        vulnerabilities = item.get("Vulnerabilities") or []
        if not isinstance(vulnerabilities, list):
            raise ValueError("Invalid Trivy JSON: Vulnerabilities must be an array")
        for raw_finding in vulnerabilities:
            finding = _as_mapping(raw_finding, "vulnerability")
            severity = finding.get("Severity")
            if severity not in {"HIGH", "CRITICAL"}:
                continue
            identifier = finding.get("VulnerabilityID")
            if not isinstance(identifier, str) or not identifier.strip():
                raise ValueError("Invalid Trivy JSON: finding has no advisory ID")
            identifiers.add(identifier)
            if severity == "HIGH":
                high += 1
            else:
                critical += 1
            fixed = finding.get("FixedVersion")
            if isinstance(fixed, str) and fixed.strip():
                with_fix += 1
            else:
                without_fix += 1

    return TrivyFindingSummary(
        high=high,
        critical=critical,
        distinct_advisories=len(identifiers),
        with_fixed_version=with_fix,
        without_fixed_version=without_fix,
    )
