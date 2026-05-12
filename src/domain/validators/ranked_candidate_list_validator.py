from __future__ import annotations

from src.domain.results.ranked_candidate import RankedCandidate


class RankedCandidateListValidator:
    """
    RankedCandidate collection contract validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        ranked_candidates: list[RankedCandidate],
    ) -> None:
        cls._validate_list_type(
            ranked_candidates,
        )

        cls._validate_not_empty(
            ranked_candidates,
        )

        cls._validate_item_types(
            ranked_candidates,
        )

    @staticmethod
    def _validate_list_type(
        ranked_candidates: object,
    ) -> None:
        if not isinstance(ranked_candidates, list):
            raise TypeError(
                "ranked_candidates must be a list."
            )

    @staticmethod
    def _validate_not_empty(
        ranked_candidates: list[RankedCandidate],
    ) -> None:
        if not ranked_candidates:
            raise ValueError(
                "ranked_candidates cannot be empty."
            )

    @staticmethod
    def _validate_item_types(
        ranked_candidates: list[RankedCandidate],
    ) -> None:
        for index, candidate in enumerate(
            ranked_candidates,
        ):
            if not isinstance(candidate, RankedCandidate):
                raise TypeError(
                    "All ranked_candidates items must be "
                    "RankedCandidate instances. "
                    f"Invalid index: {index}."
                )