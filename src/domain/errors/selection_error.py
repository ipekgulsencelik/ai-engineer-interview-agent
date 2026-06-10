from __future__ import annotations

from src.domain.errors.domain_error import DomainError


class SelectionError(DomainError):
    """Raised when question selection cannot produce a valid result."""