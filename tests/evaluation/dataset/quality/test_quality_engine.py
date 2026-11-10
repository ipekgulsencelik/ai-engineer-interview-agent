"""Behavioral tests for extensible, fail-closed dataset quality checks."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.quality import (
    AllowedValuesRule,
    DatasetQualityEngine,
    DatasetQualityError,
    IssueSeverity,
    NonEmptyStringRule,
    NumericRangeRule,
    QualityIssue,
    QualityPolicy,
    QualityReportSerializer,
    QualityRuleExecutionError,
    RequiredFieldRule,
    SchemaConformanceRule,
    UniqueFieldRule,
)
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
    DatasetRecordSchema,
)


def _engine(
    *,
    record_rules=(),
    dataset_rules=(),
    policy=None,
    max_issues: int = 10000,
) -> DatasetQualityEngine:
    class FixedClock:
        def now(self) -> datetime:
            return datetime(2026, 11, 10, tzinfo=UTC)

    return DatasetQualityEngine(
        record_rules=record_rules,
        dataset_rules=dataset_rules,
        policy=policy,
        clock=FixedClock(),
        id_factory=lambda: "run-001",
        max_issues=max_issues,
    )


def test_healthy_dataset_scores_one_and_is_accepted() -> None:
    engine = _engine(
        record_rules=(
            RequiredFieldRule(field_path="id", rule_id="required-id"),
            NumericRangeRule(
                field_path="score", minimum=0, maximum=1, rule_id="score"
            ),
        ),
        dataset_rules=(UniqueFieldRule(field_path="id", rule_id="unique-id"),),
    )
    report = engine.evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"id": "a", "score": 0.7}, {"id": "b", "score": 1.0}],
    )
    assert report.record_count == 2
    assert report.total_checks == 5
    assert report.passed_checks == 5
    assert report.failed_checks == 0
    assert report.pass_rate == 1.0
    assert report.accepted
    assert report.issues == ()
    assert report.run_id == "run-001"


def test_rule_level_checks_count_once_even_for_multiple_duplicate_issues() -> None:
    report = _engine(
        dataset_rules=(UniqueFieldRule(field_path="id"),)
    ).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"id": "same"}, {"id": "same"}, {"id": "same"}],
    )
    assert report.total_checks == 1
    assert report.failed_checks == 1
    assert report.pass_rate == 0.0
    assert report.error_count == 2
    assert report.failed_record_count == 2
    assert [issue.record_index for issue in report.issues] == [1, 2]


def test_warn_only_can_meet_policy_with_nonzero_error_allowance() -> None:
    report = _engine(
        record_rules=(
            NonEmptyStringRule(
                field_path="summary",
                severity=IssueSeverity.WARNING,
            ),
            RequiredFieldRule(field_path="id", rule_id="required-id"),
        ),
        policy=QualityPolicy(min_pass_rate=0.5, max_errors=0),
    ).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"id": "sample-1", "summary": "  "}],
    )
    assert report.warning_count == 1
    assert report.error_count == 0
    assert report.pass_rate == 0.5
    assert report.accepted


def test_strict_policy_rejects_warning_and_min_records_gate() -> None:
    rule = NonEmptyStringRule(
        field_path="summary",
        severity=IssueSeverity.WARNING,
    )
    low_quality = _engine(record_rules=(rule,)).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"summary": ""}],
    )
    assert not low_quality.accepted

    too_few = _engine(
        record_rules=(rule,), policy=QualityPolicy(
            min_pass_rate=0.0, max_errors=10, min_records=2
        )
    ).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"summary": "fine"}],
    )
    assert not too_few.accepted


def test_empty_dataset_has_zero_checks_and_fails_closed() -> None:
    report = _engine(
        record_rules=(RequiredFieldRule(field_path="id"),),
        policy=QualityPolicy(min_pass_rate=0.0, min_records=0),
    ).evaluate(dataset_id="test", dataset_version="1.0.0", records=[])
    assert report.total_checks == 0
    assert report.pass_rate == 0.0
    assert not report.accepted


@pytest.mark.parametrize(
    "record,expected",
    [
        ({"metadata": {"id": None}}, "required_field_missing"),
        ({"metadata": {"id": ""}}, "non_empty_string_invalid"),
        ({"metadata": {"id": "abc"}}, None),
    ],
)
def test_dotted_field_path_rules(
    record: dict[str, object], expected: str | None
) -> None:
    rule = RequiredFieldRule(field_path="metadata.id")
    empty = NonEmptyStringRule(
        field_path="metadata.id", rule_id="nonempty-id"
    )
    report = _engine(record_rules=(rule, empty)).evaluate(
        dataset_id="test", dataset_version="1.0.0", records=[record]
    )
    if expected is None:
        assert not report.issues
    else:
        assert any(issue.code == expected for issue in report.issues)


@pytest.mark.parametrize("value", [True, float("nan"), float("inf"), -0.1, 1.1])
def test_numeric_rule_rejects_invalid_ranges_without_value_leaks(
    value: object,
) -> None:
    report = _engine(
        record_rules=(NumericRangeRule(
            field_path="metrics.score", minimum=0, maximum=1
        ),)
    ).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"metrics": {"score": value}}],
    )
    assert not report.accepted
    assert report.issues[0].code == "numeric_out_of_range"
    assert "nan" not in report.issues[0].message


def test_allowed_values_rejects_value_without_echoing_it() -> None:
    rule = AllowedValuesRule(
        field_path="level", allowed=frozenset({"JR", "MID"})
    )
    result = rule.check(record={"level": "secret-password"}, record_index=0)
    assert len(result) == 1
    assert "secret-password" not in result[0].message


def test_schema_rule_reuses_nested_schema_validator() -> None:
    schema = DatasetRecordSchema(
        name="sample", version="1.0.0",
        fields=(
            DatasetField(
                "metadata", "object",
                properties=(DatasetField("score", "number"),)
            ),
        ),
    )
    rule = SchemaConformanceRule(schema=schema)
    report = _engine(record_rules=(rule,)).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{"metadata": {"score": "should-be-number"}}],
    )
    assert report.issues[0].code == "schema_conformance_failed"
    assert report.issues[0].field_path is None


def test_duplicate_rule_ids_rejected_across_rule_scopes() -> None:
    with pytest.raises(DatasetQualityError, match="unique"):
        _engine(
            record_rules=(RequiredFieldRule(field_path="id", rule_id="id"),),
            dataset_rules=(UniqueFieldRule(field_path="id", rule_id="id"),),
        )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"record_rules": (), "dataset_rules": ()},
        {"record_rules": [], "dataset_rules": ()},
        {"record_rules": (RequiredFieldRule(field_path="id"),), "max_issues": 0},
    ],
)
def test_invalid_engine_configuration_is_rejected(kwargs: dict) -> None:
    with pytest.raises(DatasetQualityError):
        _engine(**kwargs)


class CrashingRule:
    rule_id = "crashing"

    def check(self, *, record: Mapping[str, object], record_index: int):
        raise RuntimeError("secret data from the rule")


class InvalidIssueRule:
    rule_id = "bad-output"

    def check(self, *, record: Mapping[str, object], record_index: int):
        return (
            QualityIssue(
                rule_id="other",
                code="incorrect",
                message="invalid",
                severity=IssueSeverity.ERROR,
                record_index=record_index,
            ),
        )


class ManyIssuesRule:
    rule_id = "too-many"

    def check(self, *, records: Sequence[Mapping[str, object]]):
        return tuple(
            QualityIssue(
                rule_id=self.rule_id,
                code="duplicate",
                message="Multiple issues",
                severity=IssueSeverity.ERROR,
                record_index=index,
            )
            for index in range(len(records))
        )


def test_unexpected_rule_errors_fail_closed_and_do_not_echo_values() -> None:
    engine = _engine(record_rules=(CrashingRule(),))
    with pytest.raises(QualityRuleExecutionError, match="crashing") as raised:
        engine.evaluate(
            dataset_id="test", dataset_version="1.0.0",
            records=[{"secret": "private answer"}],
        )
    assert "private answer" not in str(raised.value)


def test_malformed_custom_rule_result_rejected() -> None:
    with pytest.raises(QualityRuleExecutionError, match="invalid issue"):
        _engine(record_rules=(InvalidIssueRule(),)).evaluate(
            dataset_id="test", dataset_version="1.0.0",
            records=[{"id": "a"}],
        )


def test_issue_count_safety_limit_blocks_unbounded_reports() -> None:
    with pytest.raises(DatasetQualityError, match="safety limit"):
        _engine(
            dataset_rules=(ManyIssuesRule(),), max_issues=2
        ).evaluate(
            dataset_id="test", dataset_version="1.0.0",
            records=[{}, {}, {}],
        )


class MutatingRule:
    rule_id = "mutator"

    def check(self, *, record: Mapping[str, object], record_index: int):
        record["list"].append("changed")
        return ()


def test_custom_rule_mutation_does_not_modify_input_records() -> None:
    records = [{"list": ["original"]}]
    before = deepcopy(records)
    _engine(record_rules=(MutatingRule(),)).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=records,
    )
    assert records == before


def test_quality_report_serializes_to_json_safe_structure() -> None:
    report = _engine(
        record_rules=(RequiredFieldRule(field_path="id"),)
    ).evaluate(
        dataset_id="test", dataset_version="1.0.0",
        records=[{}],
    )
    serialized = QualityReportSerializer.serialize(report)
    assert serialized["issues"][0]["code"] == "required_field_missing"
    assert serialized["accepted"] is False
    assert QualityReportSerializer.deserialize(serialized) == report


def test_quality_policy_invalid_values_rejected() -> None:
    for kwargs in (
        {"min_pass_rate": float("nan")},
        {"min_pass_rate": 1.1},
        {"max_errors": True},
        {"min_records": -1},
    ):
        with pytest.raises(DatasetQualityError):
            QualityPolicy(**kwargs)


def test_range_rules_validate_configuration() -> None:
    with pytest.raises(DatasetQualityError, match="minimum"):
        NumericRangeRule(field_path="score", minimum=2, maximum=1)
    with pytest.raises(DatasetQualityError, match="finite"):
        NumericRangeRule(field_path="score", minimum=float("nan"), maximum=1)
    with pytest.raises(DatasetQualityError, match="allowed"):
        AllowedValuesRule(field_path="type", allowed=frozenset())
