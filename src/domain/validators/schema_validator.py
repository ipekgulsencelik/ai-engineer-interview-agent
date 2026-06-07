from __future__ import annotations

from collections.abc import Mapping, Sized
from typing import Any

from src.domain.validation.schema_rules import (
    ValidationRule,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)
from src.domain.validation.validation_types import (
    ErrorFactory,
)
from src.domain.validators.numeric_validator import (
    NumericValidator,
)
from src.domain.validators.sequence_validator import (
    SequenceValidator,
)
from src.domain.validators.string_validator import (
    StringValidator,
)
from src.domain.validators.type_validator import (
    TypeValidator,
)


class SchemaValidator:
    """
    Generic metadata-driven schema validator.

    This class only orchestrates specialized validators.
    """

    @classmethod
    def validate_object(
        cls,
        *,
        obj: object,
        schema: SchemaDefinition,
        error_factory: ErrorFactory = ValueError,
    ) -> None:
        values: dict[str, Any] = {
            field_name: getattr(
                obj,
                field_name,
                None,
            )
            for field_name in schema
        }

        cls.validate(
            values=values,
            schema=schema,
            error_factory=error_factory,
        )

    @classmethod
    def validate(
        cls,
        *,
        values: Mapping[str, Any],
        schema: SchemaDefinition,
        error_factory: ErrorFactory = ValueError,
    ) -> None:
        for field_name, rule in schema.items():
            if field_name not in values:
                raise error_factory(
                    f"{field_name} is required."
                )

            cls._validate_field(
                field_name=field_name,
                value=values[field_name],
                rule=rule,
                error_factory=error_factory,
            )

    @classmethod
    def _validate_field(
        cls,
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if value is None:
            cls._validate_nullable(
                field_name=field_name,
                rule=rule,
                error_factory=error_factory,
            )
            return

        TypeValidator.validate(
            field_name=field_name,
            value=value,
            rule=rule,
            error_factory=error_factory,
        )

        cls._validate_bool_rejection(
            field_name=field_name,
            value=value,
            rule=rule,
            error_factory=error_factory,
        )

        cls._validate_allowed_values(
            field_name=field_name,
            value=value,
            rule=rule,
            error_factory=error_factory,
        )

        if isinstance(value, Sized):
            StringValidator.validate_non_empty(
                field_name=field_name,
                value=value,
                rule=rule,
                error_factory=error_factory,
            )

            StringValidator.validate_length_bounds(
                field_name=field_name,
                value=value,
                rule=rule,
                error_factory=error_factory,
            )

        if (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
        ):
            NumericValidator.validate_finite(
                field_name=field_name,
                value=value,
                rule=rule,
                error_factory=error_factory,
            )

            NumericValidator.validate_bounds(
                field_name=field_name,
                value=value,
                rule=rule,
                error_factory=error_factory,
            )

        SequenceValidator.validate(
            field_name=field_name,
            value=value,
            rule=rule,
            error_factory=error_factory,
        )

    @staticmethod
    def _validate_nullable(
        *,
        field_name: str,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if rule.nullable:
            return

        raise error_factory(
            f"{field_name} cannot be null."
        )

    @staticmethod
    def _validate_bool_rejection(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if rule.reject_bool and isinstance(value, bool):
            raise error_factory(
                f"{field_name} cannot be bool."
            )

    @staticmethod
    def _validate_allowed_values(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if rule.allowed_values is None:
            return

        if value not in rule.allowed_values:
            raise error_factory(
                f"{field_name} must be one of "
                f"{sorted(rule.allowed_values)}."
            )