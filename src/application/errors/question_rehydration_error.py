from __future__ import annotations


class QuestionRehydrationError(ValueError):
    """
    Raised when persisted question metadata cannot be rehydrated.
    """