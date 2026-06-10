from __future__ import annotations

import math


class RMSECalculator:
    """
    Root mean squared error calculator.
    """

    @staticmethod
    def calculate(
        *,
        mse: float,
    ) -> float:
        return math.sqrt(
            mse,
        )