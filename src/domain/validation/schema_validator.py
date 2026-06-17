from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.domain.validation.base_schema_validator import BaseSchemaValidator
from src.domain.validation.schema_types import SchemaDefinition


class SchemaValidator:
    """Schema-driven validator facade used by reporting modules."""

    @staticmethod
    def validate(
        *,
        values: dict[str, Any],
        schema: SchemaDefinition,
        error_factory: Callable[[str], Exception] = ValueError,
    ) -> None:
        for field_name, rules in schema.items():
            try:
                value = values.get(field_name)
                if value is None:
                    BaseSchemaValidator.validate_nullable(
                        field_name=field_name,
                        value=value,
                        rules=rules,
                    )
                    continue

                BaseSchemaValidator.validate_type(
                    field_name=field_name,
                    value=value,
                    rules=rules,
                )
                BaseSchemaValidator.validate_non_empty_string(
                    field_name=field_name,
                    value=value,
                    rules=rules,
                )
                BaseSchemaValidator.validate_numeric_bounds(
                    field_name=field_name,
                    value=value,
                    rules=rules,
                )
                BaseSchemaValidator.validate_tuple_items(
                    field_name=field_name,
                    value=value,
                    rules=rules,
                )
            except (TypeError, ValueError) as exc:
                raise error_factory(str(exc)) from exc
