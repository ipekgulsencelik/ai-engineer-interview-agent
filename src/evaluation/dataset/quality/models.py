"""Immutable issue, execution policy, and report domain models."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.evaluation.dataset.quality.errors import DatasetQualityError


class IssueSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True, kw_only=True)
class QualityIssue:
    rule_id: str
    code: str
    message: str
    severity: IssueSeverity
    record_index: int | None = None
    field_path: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("rule_id", "code", "message"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise DatasetQualityError(
                    f"{field_name} must be a non-empty string"
                )
        if not isinstance(self.severity, IssueSeverity):
            raise DatasetQualityError("severity must be IssueSeverity")
        if self.record_index is not None and (
            type(self.record_index) is not int or self.record_index < 0
        ):
            raise DatasetQualityError("record_index must be nonnegative")
        if self.field_path is not None and (
            not isinstance(self.field_path, str) or not self.field_path.strip()
        ):
            raise DatasetQualityError("field_path must be non-empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QualityPolicy:
    """Explicit acceptance gates; warnings contribute to check failure rate."""

    min_pass_rate: float = 1.0
    max_errors: int = 0
    min_records: int = 1

    def __post_init__(self) -> None:
        if (
            type(self.min_pass_rate) not in (int, float)
            or not math.isfinite(self.min_pass_rate)
            or not 0 <= self.min_pass_rate <= 1
        ):
            raise DatasetQualityError("min_pass_rate must be between 0 and 1")
        if type(self.max_errors) is not int or self.max_errors < 0:
            raise DatasetQualityError("max_errors must be nonnegative")
        if type(self.min_records) is not int or self.min_records < 0:
            raise DatasetQualityError("min_records must be nonnegative")


@dataclass(frozen=True, slots=True, kw_only=True)
class QualityReport:
    run_id: str
    dataset_id: str
    dataset_version: str
    checked_at: datetime
    record_count: int
    total_checks: int
    passed_checks: int
    failed_checks: int
    error_count: int
    warning_count: int
    failed_record_count: int
    pass_rate: float
    accepted: bool
    issues: tuple[QualityIssue, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.run_id, str) or not self.run_id.strip():
            raise DatasetQualityError("run_id must be non-empty")
        if not isinstance(self.dataset_id, str) or not self.dataset_id.strip():
            raise DatasetQualityError("dataset_id must be non-empty")
        if not isinstance(self.dataset_version, str) or not self.dataset_version.strip():
            raise DatasetQualityError("dataset_version must be non-empty")
        if (
            not isinstance(self.checked_at, datetime)
            or self.checked_at.tzinfo is None
            or self.checked_at.utcoffset() is None
        ):
            raise DatasetQualityError("checked_at must be timezone-aware")
        for name in (
            "record_count",
            "total_checks",
            "passed_checks",
            "failed_checks",
            "error_count",
            "warning_count",
            "failed_record_count",
        ):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise DatasetQualityError(f"{name} must be nonnegative integer")
        if self.total_checks != self.passed_checks + self.failed_checks:
            raise DatasetQualityError("check counts do not reconcile")
        if not (0 <= self.failed_record_count <= self.record_count):
            raise DatasetQualityError("invalid failed_record_count")
        expected = self.passed_checks / self.total_checks if self.total_checks else 0.0
        if (
            type(self.pass_rate) not in (float, int)
            or not math.isfinite(self.pass_rate)
            or abs(self.pass_rate - expected) > 1e-12
        ):
            raise DatasetQualityError("pass_rate does not match check counts")
        if type(self.accepted) is not bool:
            raise DatasetQualityError("accepted must be boolean")
        if not isinstance(self.issues, tuple) or not all(
            isinstance(issue, QualityIssue) for issue in self.issues
        ):
            raise DatasetQualityError("issues must be a QualityIssue tuple")
        if sum(x.severity is IssueSeverity.ERROR for x in self.issues) != self.error_count:
            raise DatasetQualityError("error_count does not match issues")
        if sum(x.severity is IssueSeverity.WARNING for x in self.issues) != self.warning_count:
            raise DatasetQualityError("warning_count does not match issues")
