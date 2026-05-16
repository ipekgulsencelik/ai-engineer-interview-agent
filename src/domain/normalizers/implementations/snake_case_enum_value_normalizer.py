from __future__ import annotations


class SnakeCaseEnumValueNormalizer:
    """
    Snake_case enum value normalization policy.
    """

    def normalize(
        self,
        *,
        value: str,
    ) -> str:
        return (
            value.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )