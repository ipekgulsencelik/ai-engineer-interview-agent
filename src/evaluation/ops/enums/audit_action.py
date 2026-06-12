from __future__ import annotations

from enum import StrEnum


class AuditAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    EVALUATE = "evaluate"
    BLOCK = "block"
    ALLOW = "allow"