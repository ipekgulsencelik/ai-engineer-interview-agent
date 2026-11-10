"""Application service for evaluation and durable report recording."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from src.evaluation.dataset.quality.models import QualityReport


class QualityEvaluatorPort(Protocol):
    def evaluate(
        self,
        *,
        dataset_id: str,
        dataset_version: str,
        records: Sequence[Mapping[str, object]],
    ) -> QualityReport: ...


class QualityReportStorePort(Protocol):
    def save(self, *, report: QualityReport) -> bool: ...


class DatasetQualityCoordinator:
    """Persist passing and failing quality evaluations for auditability."""

    def __init__(
        self,
        *,
        evaluator: QualityEvaluatorPort,
        store: QualityReportStorePort,
    ) -> None:
        self._evaluator = evaluator
        self._store = store

    def evaluate_and_store(
        self,
        *,
        dataset_id: str,
        dataset_version: str,
        records: Sequence[Mapping[str, object]],
    ) -> QualityReport:
        report = self._evaluator.evaluate(
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            records=records,
        )
        self._store.save(report=report)
        return report
