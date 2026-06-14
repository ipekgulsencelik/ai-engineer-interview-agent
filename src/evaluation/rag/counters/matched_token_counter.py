from __future__ import annotations


class MatchedTokenCounter:
    """
    Counts overlapping tokens between
    answer and chunk tokens.
    """

    @staticmethod
    def count(
        *,
        answer_tokens: set[str],
        chunk_tokens: set[str],
    ) -> int:
        return len(
            answer_tokens
            & chunk_tokens
        )