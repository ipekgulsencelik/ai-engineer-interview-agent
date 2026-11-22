"""Behavioral tests for registry-bound dataset quality evaluation."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.lineage.models import DatasetRevision
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.quality.registry_gate import (
    DatasetQualityGateError,
    RegisteredDatasetQualityGate,
)
from src.evaluation.dataset.registry.models import DatasetCatalogEntry


REVISION = DatasetRevision(dataset_id="interview-qa", version="1.0.0")
ARTIFACT = b'[{"question":"What is RAG?"}]'


def _entry(content: bytes = ARTIFACT) -> DatasetCatalogEntry:
    return DatasetCatalogEntry(
        revision=REVISION,
        content_sha256=hashlib.sha256(content).hexdigest(),
        producer="test",
        created_at=datetime(2026, 11, 23, tzinfo=UTC),
        name="Interview Questions",
        owner_id="team",
    )


def _report() -> QualityReport:
    return QualityReport(
        run_id="run-1",
        dataset_id=REVISION.dataset_id,
        dataset_version=REVISION.version,
        checked_at=datetime(2026, 11, 23, tzinfo=UTC),
        record_count=1,
        total_checks=1,
        passed_checks=1,
        failed_checks=0,
        error_count=0,
        warning_count=0,
        failed_record_count=0,
        pass_rate=1.0,
        accepted=True,
        issues=(),
    )


class Registry:
    def __init__(self, entry: DatasetCatalogEntry | None) -> None:
        self.entry = entry

    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry | None:
        assert revision == REVISION
        return self.entry


class Decoder:
    def __init__(self) -> None:
        self.calls = 0

    def decode(self, *, content: bytes):
        self.calls += 1
        assert content == ARTIFACT
        return [{"question": "What is RAG?"}]


class Evaluator:
    def __init__(self, report: QualityReport | None = None) -> None:
        self.calls = 0
        self.report = report or _report()

    def evaluate(self, *, dataset_id: str, dataset_version: str, records):
        self.calls += 1
        assert dataset_id == REVISION.dataset_id
        assert dataset_version == REVISION.version
        assert records == [{"question": "What is RAG?"}]
        return self.report


class Store:
    def __init__(self) -> None:
        self.reports: list[QualityReport] = []

    def save(self, *, report: QualityReport) -> bool:
        self.reports.append(report)
        return True


def _gate(*, entry=None, evaluator=None, decoder=None, store=None):
    actual_decoder = decoder or Decoder()
    actual_evaluator = evaluator or Evaluator()
    actual_store = store or Store()
    gate = RegisteredDatasetQualityGate(
        registry=Registry(entry),
        decoder=actual_decoder,
        evaluator=actual_evaluator,
        store=actual_store,
    )
    return gate, actual_decoder, actual_evaluator, actual_store


def test_registered_exact_artifact_evaluated_and_persisted() -> None:
    gate, decoder, evaluator, store = _gate(entry=_entry())
    report = gate.evaluate_and_store(revision=REVISION, content=ARTIFACT)
    assert report == _report()
    assert decoder.calls == evaluator.calls == 1
    assert store.reports == [report]


@pytest.mark.parametrize("entry,content", [(None, ARTIFACT), (_entry(), b"tampered")])
def test_missing_or_tampered_artifact_fails_before_decode(entry, content) -> None:
    gate, decoder, evaluator, store = _gate(entry=entry)
    with pytest.raises(DatasetQualityGateError):
        gate.evaluate_and_store(revision=REVISION, content=content)
    assert decoder.calls == evaluator.calls == 0
    assert store.reports == []


def test_quality_report_for_wrong_revision_is_never_persisted() -> None:
    evaluator = Evaluator(replace(_report(), dataset_version="2.0.0"))
    gate, _, _, store = _gate(entry=_entry(), evaluator=evaluator)
    with pytest.raises(DatasetQualityGateError, match="identity"):
        gate.evaluate_and_store(revision=REVISION, content=ARTIFACT)
    assert store.reports == []


def test_invalid_input_does_not_reach_dependencies() -> None:
    gate, decoder, evaluator, store = _gate(entry=_entry())
    with pytest.raises(DatasetQualityGateError, match="content"):
        gate.evaluate_and_store(revision=REVISION, content="not bytes")  # type: ignore[arg-type]
    assert decoder.calls == evaluator.calls == 0
    assert store.reports == []


def test_invalid_decoder_output_is_rejected_before_evaluation() -> None:
    class InvalidDecoder:
        def decode(self, *, content: bytes):
            return ["not a mapping"]

    gate, _, evaluator, store = _gate(entry=_entry(), decoder=InvalidDecoder())
    with pytest.raises(DatasetQualityGateError, match="non-mapping"):
        gate.evaluate_and_store(revision=REVISION, content=ARTIFACT)
    assert evaluator.calls == 0
    assert store.reports == []
