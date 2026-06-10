from __future__ import annotations


class UppercaseEnumValueNormalizer:
    """
    Uppercase enum value normalization policy.
    """

    def normalize(
        self,
        *,
        value: str,
    ) -> str:
        return value.strip().upper()