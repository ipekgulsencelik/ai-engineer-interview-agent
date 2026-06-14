from __future__ import annotations

from typing import Any


class WandBPayloadMapper:
    """
    Maps tracking event payloads to W&B metrics.
    """

    @staticmethod
    def numeric_payload(
        *,
        payload: dict[str, Any],
    ) -> dict[str, float]:
        return {
            key: float(value)
            for key, value in payload.items()
            if isinstance(value, int | float)
        }