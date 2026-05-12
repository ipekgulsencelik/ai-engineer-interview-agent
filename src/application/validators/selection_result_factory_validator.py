from __future__ import annotations

from src.domain.results.ranked_candidate import RankedCandidate


class SelectionResultFactoryValidator:
    """
    SelectionResultFactory input contract validation işlemlerini yapar.

    Bu validator application-level validation yapar.

    Sorumluluğu:
        - ranked_candidates listesinin geçerli olup olmadığını kontrol etmek

    Bu validator:
        - domain invariant validation yapmaz
        - selection policy çalıştırmaz
        - SelectionResult oluşturmaz
    """

    @staticmethod
    def validate_clock(
        clock: Clock,
    ) -> None:
        if not isinstance(clock, Clock):
            raise TypeError(
                "clock must be a Clock instance."
            )

            
    @classmethod
    def validate_ranked_candidates(
        cls,
        ranked_candidates: list[RankedCandidate],
    ) -> None:
        cls._validate_list_type(
            ranked_candidates,
        )

        cls._validate_not_empty(
            ranked_candidates,
        )

        cls._validate_items(
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
    def _validate_items(
        ranked_candidates: list[RankedCandidate],
    ) -> None:
        for index, candidate in enumerate(ranked_candidates):
            if not isinstance(candidate, RankedCandidate):
                raise TypeError(
                    "All ranked_candidates items must be "
                    f"RankedCandidate instances. Invalid index: {index}."
                )