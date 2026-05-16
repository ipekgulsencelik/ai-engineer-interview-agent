from __future__ import annotations


class IdentityEnumValueResolver:
    """
    Default resolver that returns the normalized value as-is.
    """

    def resolve(
        self,
        *,
        value: str,
    ) -> str:
        return value