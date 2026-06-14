from __future__ import annotations


class TextTokenizer:
    """
    Normalizes and tokenizes text.
    """

    @staticmethod
    def tokenize(
        text: str,
    ) -> set[str]:
        return {
            token.strip(
                ".,;:!?()[]{}\"'"
            ).lower()
            for token in text.split()
            if token.strip(
                ".,;:!?()[]{}\"'"
            )
        }