from __future__ import annotations


class QuestionCategoryNormalizer:
    """
    QuestionCategory canonical normalization policy.
    """

    def normalize(
        self,
        *,
        value: str,
    ) -> str:
        normalized = " ".join(
            value.strip().split()
        )

        return (
            normalized.lower()
            .replace("&", "and")
            .replace("/", "_")
            .replace("-", "_")
            .replace(" ", "_")
        )