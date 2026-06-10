from __future__ import annotations

from src.domain.errors.domain_error import DomainError


class LevelTransitionError(DomainError):
    """Raised when an adaptive level transition cannot be computed."""