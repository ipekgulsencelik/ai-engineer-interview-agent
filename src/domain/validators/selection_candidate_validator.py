from __future__ import annotations

from src.domain.errors.selection_error import (
    SelectionError,
)
from src.domain.results.selection_result import (
    SelectionResult,
)


class SelectionCandidateValidator:
    """
    Selection candidate validation helper.
    """

    @staticmethod
    def validate(
        *,
        ranked_candidates: list[SelectionResult],
    ) -> None:
        if not isinstance(ranked_candidates, list):
            raise SelectionError(
                "ranked_candidates must be a list."
            )

        if not ranked_candidates:
            raise SelectionError(
                "ranked_candidates cannot be empty."
            )

        for candidate in ranked_candidates:
            if not isinstance(candidate, SelectionResult):
                raise SelectionError(
                    "ranked_candidates must contain only SelectionResult items."
                )