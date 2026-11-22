"""Fail-closed quality evaluation of an immutable, registered artifact."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Protocol

from src.evaluation.dataset.lineage.models import DatasetRevision
from src.evaluation.dataset.quality.coordinator import (
    QualityEvaluatorPort,
    QualityReportStorePort,
)
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.registry.ports import RegistryReader


class DatasetQualityGateError(ValueError):
    """Artifact provenance or quality-report identity cannot be established."""


class DatasetArtifactDecoder(Protocol):
    """Decode the verified artifact bytes; never use unrelated caller records."""

    def decode(self, *, content: bytes) -> Sequence[Mapping[str, object]]: ...


class RegisteredDatasetQualityGate:
    """Evaluate bytes only after checking their immutable catalog identity.

    Catalog lookups, quality evaluation, and report persistence are distinct
    operations. This gate makes no distributed atomicity or freshness claim.
    """

    def __init__(
        self,
        *,
        registry: RegistryReader,
        decoder: DatasetArtifactDecoder,
        evaluator: QualityEvaluatorPort,
        store: QualityReportStorePort,
    ) -> None:
        self._registry = registry
        self._decoder = decoder
        self._evaluator = evaluator
        self._store = store

    def evaluate_and_store(
        self, *, revision: DatasetRevision, content: bytes
    ) -> QualityReport:
        if not isinstance(revision, DatasetRevision):
            raise DatasetQualityGateError("revision must be DatasetRevision")
        if not isinstance(content, bytes):
            raise DatasetQualityGateError("content must be bytes")
        entry = self._registry.get(revision=revision)
        if entry is None:
            raise DatasetQualityGateError("dataset revision is not registered")
        if hashlib.sha256(content).hexdigest() != entry.content_sha256:
            raise DatasetQualityGateError("artifact digest differs from registry")

        # Decoding verified bytes prevents caller-supplied records from being
        # substituted after provenance verification.
        records = self._decoder.decode(content=content)
        if not isinstance(records, Sequence) or isinstance(
            records, (str, bytes, bytearray)
        ):
            raise DatasetQualityGateError("decoder must return record sequence")
        if any(not isinstance(record, Mapping) for record in records):
            raise DatasetQualityGateError("decoder returned non-mapping record")

        report = self._evaluator.evaluate(
            dataset_id=revision.dataset_id,
            dataset_version=revision.version,
            records=records,
        )
        if (
            not isinstance(report, QualityReport)
            or report.dataset_id != revision.dataset_id
            or report.dataset_version != revision.version
        ):
            raise DatasetQualityGateError("quality report identity mismatch")
        self._store.save(report=report)
        return report
