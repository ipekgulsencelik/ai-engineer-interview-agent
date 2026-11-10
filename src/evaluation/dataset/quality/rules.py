"""Composable record- and dataset-scoped quality rules.

Built-in diagnostics deliberately avoid echoing sample values.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from src.evaluation.dataset.quality.errors import DatasetQualityError
from src.evaluation.dataset.quality.models import IssueSeverity, QualityIssue
from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import DatasetRecordSchema
from src.evaluation.dataset.schema_evolution.validation import DatasetRecordValidator

_MISSING = object()


def _validate_field_path(path: str) -> None:
    if (
        not isinstance(path, str)
        or not path
        or any(not fragment.strip() for fragment in path.split("."))
    ):
        raise DatasetQualityError("field_path must be a dotted field path")


def _lookup(record: Mapping[str, object], path: str) -> object:
    current: object = record
    for component in path.split("."):
        if not isinstance(current, Mapping) or component not in current:
            return _MISSING
        current = current[component]
    return current


def _issue(
    *,
    rule_id: str,
    code: str,
    message: str,
    severity: IssueSeverity,
    record_index: int | None,
    field_path: str | None,
) -> tuple[QualityIssue, ...]:
    return (
        QualityIssue(
            rule_id=rule_id,
            code=code,
            message=message,
            severity=severity,
            record_index=record_index,
            field_path=field_path,
        ),
    )


class RecordQualityRule(Protocol):
    @property
    def rule_id(self) -> str: ...

    def check(
        self, *, record: Mapping[str, object], record_index: int
    ) -> tuple[QualityIssue, ...]: ...


class DatasetQualityRule(Protocol):
    @property
    def rule_id(self) -> str: ...

    def check(
        self, *, records: Sequence[Mapping[str, object]]
    ) -> tuple[QualityIssue, ...]: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class RequiredFieldRule:
    field_path: str
    rule_id: str = "required_field"
    severity: IssueSeverity = IssueSeverity.ERROR

    def __post_init__(self) -> None:
        _validate_field_path(self.field_path)

    def check(
        self, *, record: Mapping[str, object], record_index: int
    ) -> tuple[QualityIssue, ...]:
        value = _lookup(record, self.field_path)
        if value is _MISSING or value is None:
            return _issue(
                rule_id=self.rule_id,
                code="required_field_missing",
                message="Required field is absent or null.",
                severity=self.severity,
                record_index=record_index,
                field_path=self.field_path,
            )
        return ()


@dataclass(frozen=True, slots=True, kw_only=True)
class NonEmptyStringRule:
    field_path: str
    rule_id: str = "non_empty_string"
    severity: IssueSeverity = IssueSeverity.ERROR

    def __post_init__(self) -> None:
        _validate_field_path(self.field_path)

    def check(
        self, *, record: Mapping[str, object], record_index: int
    ) -> tuple[QualityIssue, ...]:
        value = _lookup(record, self.field_path)
        if value is _MISSING:
            return ()
        if not isinstance(value, str) or not value.strip():
            return _issue(
                rule_id=self.rule_id,
                code="non_empty_string_invalid",
                message="Field must contain non-whitespace text.",
                severity=self.severity,
                record_index=record_index,
                field_path=self.field_path,
            )
        return ()


@dataclass(frozen=True, slots=True, kw_only=True)
class NumericRangeRule:
    field_path: str
    minimum: float
    maximum: float
    rule_id: str = "numeric_range"
    severity: IssueSeverity = IssueSeverity.ERROR

    def __post_init__(self) -> None:
        _validate_field_path(self.field_path)
        for name in ("minimum", "maximum"):
            value = getattr(self, name)
            if (
                type(value) not in (float, int)
                or not math.isfinite(value)
            ):
                raise DatasetQualityError(f"{name} must be finite number")
        if self.minimum > self.maximum:
            raise DatasetQualityError("minimum cannot exceed maximum")

    def check(
        self, *, record: Mapping[str, object], record_index: int
    ) -> tuple[QualityIssue, ...]:
        value = _lookup(record, self.field_path)
        if value is _MISSING:
            return ()
        if (
            type(value) not in (float, int)
            or not math.isfinite(value)
            or not self.minimum <= value <= self.maximum
        ):
            return _issue(
                rule_id=self.rule_id,
                code="numeric_out_of_range",
                message="Value is not a finite number in the accepted range.",
                severity=self.severity,
                record_index=record_index,
                field_path=self.field_path,
            )
        return ()


@dataclass(frozen=True, slots=True, kw_only=True)
class AllowedValuesRule:
    field_path: str
    allowed: frozenset[str]
    rule_id: str = "allowed_values"
    severity: IssueSeverity = IssueSeverity.ERROR

    def __post_init__(self) -> None:
        _validate_field_path(self.field_path)
        if (
            not isinstance(self.allowed, frozenset)
            or not self.allowed
            or not all(isinstance(item, str) for item in self.allowed)
        ):
            raise DatasetQualityError("allowed must be a non-empty string frozenset")

    def check(
        self, *, record: Mapping[str, object], record_index: int
    ) -> tuple[QualityIssue, ...]:
        value = _lookup(record, self.field_path)
        if value is _MISSING:
            return ()
        if not isinstance(value, str) or value not in self.allowed:
            return _issue(
                rule_id=self.rule_id,
                code="value_not_allowed",
                message="Value does not belong to the permitted set.",
                severity=self.severity,
                record_index=record_index,
                field_path=self.field_path,
            )
        return ()


@dataclass(frozen=True, slots=True, kw_only=True)
class UniqueFieldRule:
    """Dataset-wide uniqueness on present scalar values.

    Missing values are handled by a separate RequiredFieldRule.
    """

    field_path: str
    rule_id: str = "unique_field"
    severity: IssueSeverity = IssueSeverity.ERROR

    def __post_init__(self) -> None:
        _validate_field_path(self.field_path)

    def check(
        self, *, records: Sequence[Mapping[str, object]]
    ) -> tuple[QualityIssue, ...]:
        seen: set[str] = set()
        issues: list[QualityIssue] = []
        for index, record in enumerate(records):
            value = _lookup(record, self.field_path)
            if value is _MISSING:
                continue
            if (
                value is None
                or type(value) not in (str, int, float, bool)
                or (type(value) is float and not math.isfinite(value))
            ):
                issues.extend(
                    _issue(
                        rule_id=self.rule_id,
                        code="unique_field_invalid",
                        message="Unique field must have a finite scalar value.",
                        severity=self.severity,
                        record_index=index,
                        field_path=self.field_path,
                    )
                )
                continue
            key = json.dumps(
                [type(value).__name__, value], allow_nan=False
            )
            if key in seen:
                issues.extend(
                    _issue(
                        rule_id=self.rule_id,
                        code="duplicate_field_value",
                        message="Field value duplicates an earlier record.",
                        severity=self.severity,
                        record_index=index,
                        field_path=self.field_path,
                    )
                )
            seen.add(key)
        return tuple(issues)


@dataclass(frozen=True, slots=True, kw_only=True)
class SchemaConformanceRule:
    """Reuse the established nested record schema validator."""

    schema: DatasetRecordSchema
    rule_id: str = "schema_conformance"
    severity: IssueSeverity = IssueSeverity.ERROR

    def check(
        self, *, record: Mapping[str, object], record_index: int
    ) -> tuple[QualityIssue, ...]:
        try:
            DatasetRecordValidator().validate(
                schema=self.schema, record=record
            )
        except SchemaEvolutionError:
            return _issue(
                rule_id=self.rule_id,
                code="schema_conformance_failed",
                message="Record does not conform to the declared schema.",
                severity=self.severity,
                record_index=record_index,
                field_path=None,
            )
        return ()
