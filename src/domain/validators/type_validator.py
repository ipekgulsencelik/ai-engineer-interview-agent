from __future__ import annotations

from typing import Any

from src.domain.formatters.validation_formatter import (
    ValidationFormatter,
)
from src.domain.validation.schema_rules import (
    ValidationRule,
)
from src.domain.validation.validation_types import (
    ErrorFactory,
)


class TypeValidator:
    """
    Runtime type validation.
    """

    @staticmethod
    def validate(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        expected_type = rule.expected_type

        if expected_type is None:
            return

        if isinstance(
            value,
            expected_type,
        ):
            return

        raise error_factory(
            f"{field_name} must be "
            f"{ValidationFormatter.format_type_name(expected_type)}",
        )