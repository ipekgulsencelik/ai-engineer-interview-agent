from __future__ import annotations

import math


class PayloadFieldValidator:
    """
    Generic JSON payload field validation helper.
    """

    @staticmethod
    def validate_required_string(
        *,
        value: object,
        key: str,
    ) -> str:
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
    def validate_optional_string(
        *,
        value: object,
        key: str,
    ) -> str | None:
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
    def validate_required_float(
        *,
        value: object,
        key: str,
    ) -> float:
        if isinstance(value, bool):
            raise TypeError(
                f"{key} must be numeric."
            )

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{key} must be numeric."
            )

        numeric_value = float(value)

        if not math.isfinite(
            numeric_value,
        ):
            raise ValueError(
                f"{key} must be finite."
            )

        return numeric_value

    @staticmethod
    def validate_optional_string_tuple(
        *,
        value: object,
        key: str,
    ) -> tuple[str, ...] | None:
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