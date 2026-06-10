from __future__ import annotations

from collections.abc import Sequence


class PairedDifferenceCalculator:
    """
    Calculates paired differences.
    """

    @staticmethod
    def calculate(
        *,
        before_values: Sequence[float],
        after_values: Sequence[float],
    ) -> tuple[float, ...]:
        return tuple(
            after - before
            for before, after in zip(
                before_values,
                after_values,
                strict=True,
            )
        )