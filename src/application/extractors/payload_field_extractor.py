from __future__ import annotations

import math
from typing import Any


class PayloadFieldExtractor:
    """
    JSON payload içinden strongly-validated field extraction yapar.

    Bu sınıf:
        - primitive değerleri normalize eder
        - type validation yapar
        - business fallback uygulamaz
        - domain object üretmez
    """

    @staticmethod
    def get_required_string(
        payload: dict[str, Any],
        key: str,
    ) -> str:
        value = payload.get(key)

        if not isinstance(value, str):
            raise TypeError(
                f"{key} must be a string."
            )

        normalized = value.strip()

        if not normalized:
            raise ValueError(
                f"{key} cannot be empty."
            )

        return normalized

    @staticmethod
    def get_optional_string(
        payload: dict[str, Any],
        key: str,
    ) -> str | None:
        value = payload.get(key)

        if value is None:
            return None

        if not isinstance(value, str):
            raise TypeError(
                f"{key} must be a string."
            )

        normalized = value.strip()

        if not normalized:
            raise ValueError(
                f"{key} cannot be empty."
            )

        return normalized

    @staticmethod
    def get_required_float(
        payload: dict[str, Any],
        key: str,
    ) -> float:
        value = payload.get(key)

        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise TypeError(
                f"{key} must be numeric."
            )

        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise ValueError(
                f"{key} must be finite."
            )

        return numeric_value

    @classmethod
    def get_optional_float(
        cls,
        payload: dict[str, Any],
        key: str,
    ) -> float | None:
        value = payload.get(key)

        if value is None:
            return None

        return cls.get_required_float(
            payload,
            key,
        )

    @staticmethod
    def get_optional_string_tuple(
        payload: dict[str, Any],
        key: str,
    ) -> tuple[str, ...] | None:
        value = payload.get(key)

        if value is None:
            return None

        if not isinstance(value, list):
            raise TypeError(
                f"{key} must be a list."
            )

        normalized_items: list[str] = []

        for item in value:
            if not isinstance(item, str):
                raise TypeError(
                    f"All items in {key} must be strings."
                )

            normalized_item = item.strip()

            if not normalized_item:
                raise ValueError(
                    f"Items in {key} cannot be empty."
                )

            normalized_items.append(
                normalized_item,
            )

        return tuple(normalized_items)