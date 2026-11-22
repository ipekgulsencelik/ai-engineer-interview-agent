"""Read-only dataset catalog governance with fail-closed durable auditing.

This service is not an authentication system, general-purpose PDP, or data
erasure engine. Caller-provided catalog owner metadata never grants access.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol
from uuid import uuid4

from src.evaluation.dataset.lineage.models import DatasetRevision
from src.evaluation.dataset.registry.models import DatasetCatalogEntry
from src.evaluation.dataset.registry.ports import RegistryReader


class DatasetGovernanceError(RuntimeError):
    """The authorization or audit contract cannot be satisfied."""


class DatasetCatalogAccessDenied(DatasetGovernanceError):
    """Catalog access is denied; no resource existence is disclosed."""


class CatalogRole(StrEnum):
    READER = "reader"
    STEWARD = "steward"


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifiedCatalogIdentity:
    """Only an authenticated, trusted adapter may construct this identity."""

    principal_id: str
    tenant_id: str
    roles: frozenset[CatalogRole]

    def __post_init__(self) -> None:
        for field in ("principal_id", "tenant_id"):
            val = getattr(self, field)
            if not isinstance(val, str) or not val.strip() or len(val) > 128:
                raise DatasetGovernanceError(f"{field} must be 1..128 characters")
        if not isinstance(self.roles, frozenset) or any(
            not isinstance(role, CatalogRole) for role in self.roles
        ):
            raise DatasetGovernanceError("roles must contain trusted CatalogRole")


@dataclass(frozen=True, slots=True, kw_only=True)
class CatalogAccessPolicy:
    """Authoritative, external dataset-to-tenant role mapping, not owner_id."""

    dataset_id: str
    tenant_id: str
    allowed_roles: frozenset[CatalogRole]
    access_expires_at: datetime | None = None

    def __post_init__(self) -> None:
        for field in ("dataset_id", "tenant_id"):
            val = getattr(self, field)
            if not isinstance(val, str) or not val.strip() or len(val) > 128:
                raise DatasetGovernanceError(f"{field} must be 1..128 characters")
        if not isinstance(self.allowed_roles, frozenset) or any(
            not isinstance(role, CatalogRole) for role in self.allowed_roles
        ):
            raise DatasetGovernanceError("allowed_roles must contain CatalogRole")
        expires = self.access_expires_at
        if expires is not None and (
            not isinstance(expires, datetime)
            or expires.tzinfo is None
            or expires.utcoffset() is None
        ):
            raise DatasetGovernanceError("expiry must be timezone-aware")


@dataclass(frozen=True, slots=True, kw_only=True)
class CatalogAccessAuditEvent:
    event_id: str
    principal_id: str
    tenant_id: str
    dataset_id: str
    version: str
    occurred_at: datetime
    allowed: bool
    reason_code: str

    def __post_init__(self) -> None:
        for field in (
            "event_id", "principal_id", "tenant_id", "dataset_id",
            "version", "reason_code",
        ):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip() or len(value) > 128:
                raise DatasetGovernanceError("audit identity is invalid")
        if not isinstance(self.allowed, bool):
            raise DatasetGovernanceError("audit decision must be boolean")
        if (
            not isinstance(self.occurred_at, datetime)
            or self.occurred_at.tzinfo is None
            or self.occurred_at.utcoffset() is None
        ):
            raise DatasetGovernanceError("audit time must be timezone-aware")


class VerifiedIdentityPort(Protocol):
    def current(self) -> VerifiedCatalogIdentity: ...


class CatalogPolicyPort(Protocol):
    def get_policy(self, *, dataset_id: str) -> CatalogAccessPolicy | None: ...


class CatalogAuditPort(Protocol):
    def append(self, *, event: CatalogAccessAuditEvent) -> bool: ...


class CatalogClock(Protocol):
    def now(self) -> datetime: ...


class SystemCatalogClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class GovernedDatasetCatalogReader:
    """Protect individual catalog metadata lookups; audit before returning.

    All catalog callers must use this facade. The underlying RegistryReader
    remains unrestricted for internal system processes: DI/composition must
    prevent untrusted code from receiving that lower-level port directly.
    """

    def __init__(
        self,
        *,
        registry: RegistryReader,
        identity: VerifiedIdentityPort,
        policies: CatalogPolicyPort,
        audit: CatalogAuditPort,
        clock: CatalogClock | None = None,
        event_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._registry = registry
        self._identity = identity
        self._policies = policies
        self._audit = audit
        self._clock = clock if clock is not None else SystemCatalogClock()
        self._event_id_factory = (
            event_id_factory if event_id_factory is not None else lambda: uuid4().hex
        )

    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry:
        if not isinstance(revision, DatasetRevision):
            raise DatasetGovernanceError("revision must be DatasetRevision")
        principal = self._identity.current()
        if not isinstance(principal, VerifiedCatalogIdentity):
            raise DatasetGovernanceError("trusted identity adapter returned invalid type")
        now = self._clock.now()
        if (
            not isinstance(now, datetime)
            or now.tzinfo is None
            or now.utcoffset() is None
        ):
            raise DatasetGovernanceError("clock must be timezone-aware")

        policy = self._policies.get_policy(dataset_id=revision.dataset_id)
        if policy is not None and not isinstance(policy, CatalogAccessPolicy):
            raise DatasetGovernanceError("policy provider returned invalid type")
        reason: str
        entry: DatasetCatalogEntry | None = None
        if policy is None or policy.dataset_id != revision.dataset_id:
            reason = "policy_missing"
        elif policy.tenant_id != principal.tenant_id:
            reason = "tenant_mismatch"
        elif not principal.roles.intersection(policy.allowed_roles):
            reason = "role_denied"
        elif policy.access_expires_at is not None and now >= policy.access_expires_at:
            reason = "access_expired"
        else:
            # Only access catalog metadata after a trusted policy allows it.
            entry = self._registry.get(revision=revision)
            if entry is None:
                reason = "not_found"
            elif entry.revision != revision:
                raise DatasetGovernanceError("registry returned wrong revision")
            else:
                reason = "allowed"
        event = CatalogAccessAuditEvent(
            event_id=self._event_id_factory(),
            principal_id=principal.principal_id,
            tenant_id=principal.tenant_id,
            dataset_id=revision.dataset_id,
            version=revision.version,
            occurred_at=now,
            allowed=reason == "allowed",
            reason_code=reason,
        )
        # Audit loss blocks metadata disclosure. Durable store must return True
        # only after an append transaction successfully commits.
        if self._audit.append(event=event) is not True:
            raise DatasetGovernanceError("durable audit was not acknowledged")
        if entry is None:
            raise DatasetCatalogAccessDenied("catalog access denied")
        return entry
