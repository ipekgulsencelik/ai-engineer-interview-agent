"""Fail-closed, deterministic batch quality validation orchestration."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from src.evaluation.dataset.quality.errors import (
    DatasetQualityError,
    QualityRuleExecutionError,
)
from src.evaluation.dataset.quality.models import (
    IssueSeverity,
    QualityIssue,
    QualityPolicy,
    QualityReport,
)
from src.evaluation.dataset.quality.rules import (
    DatasetQualityRule,
    RecordQualityRule,
)
from src.evaluation.dataset.schema_evolution.models import parse_schema_version


class QualityClock(Protocol):
    def now(self) -> datetime: ...


class SystemQualityClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class DatasetQualityEngine:
    """Orchestrate independently testable rule implementations.

    An issue marks its producing check as failed, even for warning severity.
    Dataset-level checks count once per dataset, not once per record.
    """

    def __init__(
        self,
        *,
        record_rules: tuple[RecordQualityRule, ...] = (),
        dataset_rules: tuple[DatasetQualityRule, ...] = (),
        policy: QualityPolicy | None = None,
        clock: QualityClock | None = None,
        id_factory: Callable[[], str] | None = None,
        max_issues: int = 10000,
    ) -> None:
        if not isinstance(record_rules, tuple) or not isinstance(
            dataset_rules, tuple
        ):
            raise DatasetQualityError("rule collections must be tuples")
        if type(max_issues) is not int or max_issues < 1:
            raise DatasetQualityError("max_issues must be a positive integer")
        all_rules: tuple[RecordQualityRule | DatasetQualityRule, ...] = (
            *record_rules, *dataset_rules
        )
        if not all_rules:
            raise DatasetQualityError("at least one quality rule is required")
        identifiers: list[str] = []
        for rule in all_rules:
            identifier = getattr(rule, "rule_id", None)
            if not isinstance(identifier, str) or not identifier.strip():
                raise DatasetQualityError("every rule requires a non-empty rule_id")
            if not callable(getattr(rule, "check", None)):
                raise DatasetQualityError("every rule must implement check")
            identifiers.append(identifier)
        if len(identifiers) != len(set(identifiers)):
            raise DatasetQualityError("quality rule_id values must be unique")

        self._record_rules = record_rules
        self._dataset_rules = dataset_rules
        self._policy = policy if policy is not None else QualityPolicy()
        self._clock = clock if clock is not None else SystemQualityClock()
        self._id_factory = (
            id_factory if id_factory is not None else lambda: uuid4().hex
        )
        self._max_issues = max_issues

    def evaluate(
        self,
        *,
        dataset_id: str,
        dataset_version: str,
        records: Sequence[Mapping[str, object]],
    ) -> QualityReport:
        if not isinstance(dataset_id, str) or not dataset_id.strip():
            raise DatasetQualityError("dataset_id must be non-empty")
        parse_schema_version(dataset_version)
        if not isinstance(records, Sequence) or isinstance(
            records, (str, bytes)
        ):
            raise DatasetQualityError("records must be a sequence of mappings")
        for index, record in enumerate(records):
            if not isinstance(record, Mapping):
                raise DatasetQualityError(
                    f"record[{index}] must be a mapping"
                )

        # Deep copies also isolate caller data from side effects in custom rules.
        snapshot = tuple(deepcopy(dict(record)) for record in records)
        issues: list[QualityIssue] = []
        checked = 0
        failed = 0

        for index, record in enumerate(snapshot):
            for rule in self._record_rules:
                result = self._invoke_record_rule(
                    rule=rule, record=deepcopy(record), index=index
                )
                self._verify_result(
                    result=result,
                    rule_id=rule.rule_id,
                    record_count=len(snapshot),
                    expected_index=index,
                )
                checked += 1
                if result:
                    failed += 1
                    issues.extend(result)
                    self._check_issue_limit(len(issues))

        for rule in self._dataset_rules:
            result = self._invoke_dataset_rule(
                rule=rule, records=deepcopy(snapshot)
            )
            self._verify_result(
                result=result,
                rule_id=rule.rule_id,
                record_count=len(snapshot),
                expected_index=None,
            )
            checked += 1
            if result:
                failed += 1
                issues.extend(result)
                self._check_issue_limit(len(issues))

        errors = sum(issue.severity is IssueSeverity.ERROR for issue in issues)
        warnings = sum(issue.severity is IssueSeverity.WARNING for issue in issues)
        failed_records = len({
            issue.record_index
            for issue in issues
            if issue.record_index is not None
        })
        passed = checked - failed
        pass_rate = passed / checked if checked else 0.0
        accepted = (
            len(snapshot) >= self._policy.min_records
            and checked > 0
            and pass_rate >= self._policy.min_pass_rate
            and errors <= self._policy.max_errors
        )
        return QualityReport(
            run_id=self._id_factory(),
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            checked_at=self._clock.now(),
            record_count=len(snapshot),
            total_checks=checked,
            passed_checks=passed,
            failed_checks=failed,
            error_count=errors,
            warning_count=warnings,
            failed_record_count=failed_records,
            pass_rate=pass_rate,
            accepted=accepted,
            issues=tuple(issues),
        )

    def _check_issue_limit(self, count: int) -> None:
        if count > self._max_issues:
            raise DatasetQualityError(
                "issue count exceeds configured safety limit"
            )

    @staticmethod
    def _invoke_record_rule(
        *,
        rule: RecordQualityRule,
        record: Mapping[str, object],
        index: int,
    ) -> tuple[QualityIssue, ...]:
        try:
            return rule.check(record=record, record_index=index)
        except Exception as exc:
            raise QualityRuleExecutionError(
                f"record rule {rule.rule_id} failed to execute"
            ) from exc

    @staticmethod
    def _invoke_dataset_rule(
        *,
        rule: DatasetQualityRule,
        records: Sequence[Mapping[str, object]],
    ) -> tuple[QualityIssue, ...]:
        try:
            return rule.check(records=records)
        except Exception as exc:
            raise QualityRuleExecutionError(
                f"dataset rule {rule.rule_id} failed to execute"
            ) from exc

    @staticmethod
    def _verify_result(
        *,
        result: object,
        rule_id: str,
        record_count: int,
        expected_index: int | None,
    ) -> None:
        if not isinstance(result, tuple):
            raise QualityRuleExecutionError(
                f"rule {rule_id} returned non-tuple violations"
            )
        for issue in result:
            if not isinstance(issue, QualityIssue) or issue.rule_id != rule_id:
                raise QualityRuleExecutionError(
                    f"rule {rule_id} returned invalid issue"
                )
            if expected_index is not None and issue.record_index != expected_index:
                raise QualityRuleExecutionError(
                    f"record rule {rule_id} returned incorrect index"
                )
            if issue.record_index is not None and issue.record_index >= record_count:
                raise QualityRuleExecutionError(
                    f"rule {rule_id} returned out-of-bounds record index"
                )
