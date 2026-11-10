"""Lossless, machine-readable quality report serialization."""

from __future__ import annotations

from typing import Any

from src.evaluation.dataset.quality.models import (
    IssueSeverity,
    QualityIssue,
    QualityReport,
)


class QualityReportSerializer:
    """Stable JSON-safe report projection, never includes input records."""

    @staticmethod
    def serialize(report: QualityReport) -> dict[str, Any]:
        return {
            "run_id": report.run_id,
            "dataset_id": report.dataset_id,
            "dataset_version": report.dataset_version,
            "checked_at": report.checked_at.isoformat(),
            "record_count": report.record_count,
            "total_checks": report.total_checks,
            "passed_checks": report.passed_checks,
            "failed_checks": report.failed_checks,
            "error_count": report.error_count,
            "warning_count": report.warning_count,
            "failed_record_count": report.failed_record_count,
            "pass_rate": report.pass_rate,
            "accepted": report.accepted,
            "issues": [
                {
                    "rule_id": issue.rule_id,
                    "code": issue.code,
                    "message": issue.message,
                    "severity": issue.severity.value,
                    "record_index": issue.record_index,
                    "field_path": issue.field_path,
                }
                for issue in report.issues
            ],
        }

    @staticmethod
    def deserialize(payload: dict[str, Any]) -> QualityReport:
        from datetime import datetime

        return QualityReport(
            run_id=payload["run_id"],
            dataset_id=payload["dataset_id"],
            dataset_version=payload["dataset_version"],
            checked_at=datetime.fromisoformat(payload["checked_at"]),
            record_count=payload["record_count"],
            total_checks=payload["total_checks"],
            passed_checks=payload["passed_checks"],
            failed_checks=payload["failed_checks"],
            error_count=payload["error_count"],
            warning_count=payload["warning_count"],
            failed_record_count=payload["failed_record_count"],
            pass_rate=payload["pass_rate"],
            accepted=payload["accepted"],
            issues=tuple(
                QualityIssue(
                    rule_id=issue["rule_id"],
                    code=issue["code"],
                    message=issue["message"],
                    severity=IssueSeverity(issue["severity"]),
                    record_index=issue["record_index"],
                    field_path=issue["field_path"],
                )
                for issue in payload["issues"]
            ),
        )
