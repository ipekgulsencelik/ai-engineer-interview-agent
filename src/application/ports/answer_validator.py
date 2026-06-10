from __future__ import annotations

from typing import Protocol


class AnswerValidator(Protocol):
    """
    Candidate answer validation contract.
    """

    def validate(
        self,
        answer: str,
    ) -> None:
        """
        Raw candidate answer'ı validate eder.
        """
        ...