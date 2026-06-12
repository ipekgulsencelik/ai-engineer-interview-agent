from __future__ import annotations

from uuid import uuid4


class RunIdProvider:
    """
    Run identifier provider.
    """

    @staticmethod
    def generate() -> str:
        return str(
            uuid4(),
        )