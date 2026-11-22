"""Governance read boundary and durable audit security regressions."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

from src.evaluation.dataset.governance import (
    CatalogAccessPolicy,
    CatalogRole,
    DatasetCatalogAccessDenied,
    DatasetGovernanceError,
    GovernedDatasetCatalogReader,
    VerifiedCatalogIdentity,
)
from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)
from src.evaluation.dataset.registry import DatasetRegistryService
from src.evaluation.dataset.registry.models import DatasetCatalogEntry
from src.infrastructure.repositories.sqlite_dataset_governance_audit_repository import (
    SQLiteDatasetGovernanceAuditRepository,
)
from src.infrastructure.repositories.sqlite_dataset_lineage_repository import (
    SQLiteDatasetLineageRepository,
)
from src.infrastructure.repositories.sqlite_dataset_registry_repository import (
    SQLiteDatasetRegistryRepository,
)


NOW = datetime(2026, 11, 23, tzinfo=UTC)
REVISION = DatasetRevision(dataset_id="interview-qa", version="1.0.0")


def _entry() -> DatasetCatalogEntry:
    return DatasetCatalogEntry(
        revision=REVISION,
        content_sha256="a" * 64,
        producer="tests",
        created_at=NOW,
        name="Interview questions",
        owner_id="untrusted-owner-not-an-authorization",
    )


class Identity:
    def __init__(
        self, *, tenant: str = "tenant-a", roles=None
    ) -> None:
        self.value = VerifiedCatalogIdentity(
            principal_id="opaque-actor-1",
            tenant_id=tenant,
            roles=roles if roles is not None else frozenset({CatalogRole.READER}),
        )

    def current(self) -> VerifiedCatalogIdentity:
        return self.value


class Policies:
    def __init__(
        self, policy: CatalogAccessPolicy | None
    ) -> None:
        self.policy = policy

    def get_policy(self, *, dataset_id: str) -> CatalogAccessPolicy | None:
        assert dataset_id == "interview-qa"
        return self.policy


class Registry:
    def __init__(self, entry: DatasetCatalogEntry | None = None) -> None:
        self.value = entry
        self.reads = 0

    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry | None:
        self.reads += 1
        return self.value

    def list_versions(self, *, dataset_id: str, limit: int = 100):
        return ()

    def list_by_tag(self, *, tag: str, limit: int = 100):
        return ()


class Clock:
    def now(self) -> datetime:
        return NOW


def _policy(
    *, tenant: str = "tenant-a",
    roles: frozenset[CatalogRole] = frozenset({CatalogRole.READER}),
    expiry: datetime | None = None,
) -> CatalogAccessPolicy:
    return CatalogAccessPolicy(
        dataset_id="interview-qa",
        tenant_id=tenant,
        allowed_roles=roles,
        access_expires_at=expiry,
    )


def _reader(
    tmp_path,
    *,
    policy: CatalogAccessPolicy | None = None,
    identity: Identity | None = None,
    registry: Registry | None = None,
    audit=None,
):
    store = audit or SQLiteDatasetGovernanceAuditRepository(
        tmp_path / "catalog-audit.sqlite"
    )
    res = registry if registry is not None else Registry(_entry())
    return (
        GovernedDatasetCatalogReader(
            registry=res,
            identity=identity or Identity(),
            policies=Policies(policy if policy is not None else _policy()),
            audit=store,
            clock=Clock(),
            event_id_factory=lambda: "event-1",
        ),
        store,
        res,
    )


def test_authorized_reader_returns_catalog_and_audits_before_return(tmp_path):
    reader, store, _ = _reader(tmp_path)
    assert reader.get(revision=REVISION) == _entry()
    events = store.list_events(dataset_id="interview-qa")
    assert len(events) == 1
    assert events[0].allowed
    assert events[0].reason_code == "allowed"
    assert events[0].principal_id == "opaque-actor-1"
    assert not hasattr(events[0], "description")
    assert not hasattr(events[0], "content_sha256")


@pytest.mark.parametrize(
    ("identity", "policy", "reason"),
    [
        (Identity(tenant="tenant-b"), _policy(), "tenant_mismatch"),
        (Identity(roles=frozenset()), _policy(), "role_denied"),
        (Identity(), _policy(roles=frozenset({CatalogRole.STEWARD})), "role_denied"),
        (Identity(), _policy(expiry=NOW), "access_expired"),
        (Identity(), _policy(expiry=NOW - timedelta(seconds=1)), "access_expired"),
        (Identity(), _policy(tenant="tenant-b"), "tenant_mismatch"),
    ],
)
def test_denials_are_audited_without_loading_catalog(
    tmp_path, identity, policy, reason
):
    reader, store, registry = _reader(
        tmp_path, identity=identity, policy=policy
    )
    with pytest.raises(DatasetCatalogAccessDenied, match="access denied"):
        reader.get(revision=REVISION)
    assert registry.reads == 0
    assert store.list_events(dataset_id="interview-qa")[0].reason_code == reason


def test_missing_authoritative_policy_is_denied_and_logged(tmp_path):
    store = SQLiteDatasetGovernanceAuditRepository(tmp_path / "audit.sqlite")
    registry = Registry(_entry())
    reader = GovernedDatasetCatalogReader(
        registry=registry,
        identity=Identity(),
        policies=Policies(None),
        audit=store,
        clock=Clock(),
        event_id_factory=lambda: "missing-policy-event",
    )
    with pytest.raises(DatasetCatalogAccessDenied):
        reader.get(revision=REVISION)
    assert registry.reads == 0
    assert store.list_events(
        dataset_id="interview-qa"
    )[0].reason_code == "policy_missing"


def test_missing_record_is_not_disclosed_and_is_logged(tmp_path):
    reader, store, registry = _reader(tmp_path, registry=Registry())
    with pytest.raises(DatasetCatalogAccessDenied):
        reader.get(revision=REVISION)
    assert registry.reads == 1
    event = store.list_events(dataset_id="interview-qa")[0]
    assert not event.allowed
    assert event.reason_code == "not_found"


def test_failed_audit_refuses_to_return_authorized_data(tmp_path):
    class BrokenAudit:
        def append(self, *, event):
            raise DatasetGovernanceError("audit write rejected")

    reader, _, _ = _reader(tmp_path, audit=BrokenAudit())
    with pytest.raises(DatasetGovernanceError, match="audit write"):
        reader.get(revision=REVISION)


def test_unacknowledged_audit_refuses_to_return_authorized_data(tmp_path):
    class SilentAudit:
        def append(self, *, event):
            return False

    reader, _, _ = _reader(tmp_path, audit=SilentAudit())
    with pytest.raises(DatasetGovernanceError, match="not acknowledged"):
        reader.get(revision=REVISION)


def test_file_backed_audit_is_append_only_and_reopens(tmp_path):
    path = tmp_path / "audit.sqlite"
    reader, store, _ = _reader(
        tmp_path, audit=SQLiteDatasetGovernanceAuditRepository(path)
    )
    assert reader.get(revision=REVISION) == _entry()
    restarted = SQLiteDatasetGovernanceAuditRepository(path)
    assert restarted.list_events(dataset_id="interview-qa") == store.list_events(
        dataset_id="interview-qa"
    )
    # The fixed event ID intentionally fails rather than replacing audit history.
    with pytest.raises(DatasetGovernanceError, match="append"):
        reader.get(revision=REVISION)
    assert len(restarted.list_events(dataset_id="interview-qa")) == 1


def test_corrupted_event_checksum_blocks_audit_history(tmp_path):
    reader, store, _ = _reader(tmp_path)
    assert reader.get(revision=REVISION)
    with sqlite3.connect(tmp_path / "catalog-audit.sqlite") as conn:
        conn.execute(
            """
            UPDATE dataset_catalog_access_events SET event_json='{}'
            WHERE event_id='event-1'
            """
        )
    with pytest.raises(DatasetGovernanceError, match="checksum"):
        store.list_events(dataset_id="interview-qa")


def test_invalid_policy_and_identity_shapes_rejected():
    with pytest.raises(DatasetGovernanceError, match="roles"):
        VerifiedCatalogIdentity(
            principal_id="id", tenant_id="a", roles=frozenset({"admin"})
        )
    with pytest.raises(DatasetGovernanceError, match="expiry"):
        _policy(expiry=datetime(2026, 11, 23))
    with pytest.raises(DatasetGovernanceError, match="allowed_roles"):
        _policy(roles=frozenset({"superuser"}))


def test_audit_does_not_contain_catalog_description_or_raw_artifact(tmp_path):
    reader, _, _ = _reader(tmp_path)
    reader.get(revision=REVISION)
    data = (tmp_path / "catalog-audit.sqlite").read_bytes()
    assert b"untrusted-owner-not-an-authorization" not in data
    assert b"Interview questions" not in data
    assert b"DO-NOT-STORE-CANDIDATE-ANSWER" not in data



def test_real_lineage_registry_read_through_governance(tmp_path):
    lineage = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    catalog = SQLiteDatasetRegistryRepository(tmp_path / "catalog.sqlite")
    node = DatasetLineageNode.from_artifact(
        revision=REVISION,
        content=b"source bytes, never returned by catalog",
        producer="trusted-publisher",
        created_at=NOW,
    )
    lineage.register(node=node, parents=())
    DatasetRegistryService(lineage=lineage, registry=catalog).register(
        node=node, name="Interview QA", owner_id="owner-is-not-authorization"
    )
    audit = SQLiteDatasetGovernanceAuditRepository(
        tmp_path / "governance.sqlite"
    )
    governed = GovernedDatasetCatalogReader(
        registry=catalog,
        identity=Identity(),
        policies=Policies(_policy()),
        audit=audit,
        clock=Clock(),
        event_id_factory=lambda: "actual-registry-read-1",
    )
    entry = governed.get(revision=REVISION)
    assert entry.revision == REVISION
    assert entry.content_sha256 == node.content_sha256
    assert not hasattr(entry, "content")
    assert audit.list_events(dataset_id="interview-qa")[0].allowed
