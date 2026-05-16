from __future__ import annotations

from src.domain.errors.validation_error import (
    ValidationError,
)


class QuestionValidationError(ValidationError):
    """
    Raised when Question entity validation fails.
    """