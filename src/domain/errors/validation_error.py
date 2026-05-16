from __future__ import annotations

from src.domain.errors.domain_error import DomainError


class ValidationError(DomainError):
    """
    Base validation error.
    """