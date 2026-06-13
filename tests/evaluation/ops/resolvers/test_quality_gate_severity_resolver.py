from __future__ import annotations

from src.evaluation.ops.resolvers.quality_gate_severity_resolver import (
    QualityGateSeverityResolver,
)


def test_quality_gate_severity_resolver_should_return_info_for_passed_gate() -> None:
    assert QualityGateSeverityResolver.resolve(passed=True) == "info"


def test_quality_gate_severity_resolver_should_return_critical_for_failed_gate() -> (
    None
):
    assert QualityGateSeverityResolver.resolve(passed=False) == "critical"
