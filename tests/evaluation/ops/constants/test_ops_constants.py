from __future__ import annotations

from src.evaluation.ops.constants.ci_policy import MINIMUM_OVERALL_SCORE_GATE_NAME
from src.evaluation.ops.constants.quality_gates import (
    QUALITY_GATE_CRITICAL_SEVERITY,
    QUALITY_GATE_INFO_SEVERITY,
    QUALITY_GATE_WARNING_SEVERITY,
    VALID_QUALITY_GATE_SEVERITIES,
)


def test_ci_policy_constants_should_define_minimum_score_gate_name() -> None:
    assert MINIMUM_OVERALL_SCORE_GATE_NAME == "minimum_overall_score"


def test_quality_gate_constants_should_include_all_valid_severities() -> None:
    assert VALID_QUALITY_GATE_SEVERITIES == {
        QUALITY_GATE_INFO_SEVERITY,
        QUALITY_GATE_WARNING_SEVERITY,
        QUALITY_GATE_CRITICAL_SEVERITY,
    }
