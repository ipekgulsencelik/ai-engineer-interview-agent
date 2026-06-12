from __future__ import annotations

from typing import TypeAlias


AuditMetadataValue: TypeAlias = (
    str | int | float | bool
)

AuditMetadata: TypeAlias = dict[
    str,
    AuditMetadataValue,
]