from __future__ import annotations

from collections.abc import Sized

from src.domain.validation.schema_rules import (
    ValidationRule,
)
from src.domain.validation.validation_types import (
    ErrorFactory,
)


class StringValidator:
    """
    String and length validation utilities.
    """

    @staticmethod
    def validate_non_empty(
        *,
        field_name: str,
        value: Sized,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if not rule.non_empty:
            return

        checked_value = (
            value.strip()
            if isinstance(value, str)
            and rule.strip
            else value
        )

        if len(checked_value) == 0:
            raise error_factory(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def validate_length_bounds(
        *,
        field_name: str,
        value: Sized,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if (
            rule.min_length is None
            and rule.max_length is None
        ):
            return

        checked_value = (
            value.strip()
            if isinstance(value, str)
            and rule.strip
            else value
        )

        length = len(checked_value)

        if (
            rule.min_length is not None
            and length < rule.min_length
        ):
            raise error_factory(
                f"{field_name} length must be at least "
                f"{rule.min_length}."
            )

        if (
            rule.max_length is not None
            and length > rule.max_length
        ):
            raise error_factory(
                f"{field_name} length must be at most "
                f"{rule.max_length}."
            )