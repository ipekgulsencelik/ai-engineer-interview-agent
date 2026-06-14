from __future__ import annotations


class ChunkAttributionScoreCalculator:
    """
    Calculates chunk attribution score.
    """

    @staticmethod
    def calculate(
        *,
        matched_tokens: int,
        answer_token_count: int,
    ) -> float:
        if answer_token_count == 0:
            return 0.0

        return (
            matched_tokens
            / answer_token_count
        )