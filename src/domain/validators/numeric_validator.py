from __future__ import annotations

import math

from src.domain.validation.schema_rules import (
    ValidationRule,
)
from src.domain.validation.validation_types import (
    ErrorFactory,
)


class NumericValidator:
    """
    Numeric validation utilities.
    """

    @staticmethod
    def validate_finite(
        *,
        field_name: str,
        value: int | float,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if not rule.finite:
            return

        if isinstance(
            value,
            bool,
        ):
            return

        if not math.isfinite(
            value,
        ):
            raise error_factory(
                f"{field_name} must be finite."
            )

    @staticmethod
    def validate_bounds(
        *,
        field_name: str,
        value: int | float,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if isinstance(
            value,
            bool,
        ):
            return

        if (
            rule.min_value is not None
            and value < rule.min_value
        ):
            raise error_factory(
                f"{field_name} must be greater than "
                f"or equal to {rule.min_value}."
            )

        if (
            rule.max_value is not None
            and value > rule.max_value
        ):
            raise error_factory(
                f"{field_name} must be less than "
                f"or equal to {rule.max_value}."
            )