from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any, Final

from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


COLLECTION_TYPES: Final[tuple[type, ...]] = (
    list,
    tuple,
    set,
    frozenset,
)

SIZED_TYPES: Final[tuple[type, ...]] = (
    str,
    list,
    tuple,
    set,
    frozenset,
    Mapping,
)


class SchemaValidator:
    """
    Schema-driven object and mapping validator.
    """

    @classmethod
    def validate_object(
        cls,
        *,
        obj: object,
        schema: ValidationSchema,
    ) -> None:
        """
        Validate an object's attributes against a validation schema.
        """

        data = {
            field_name: getattr(
                obj,
                field_name,
                None,
            )
            for field_name in schema
        }

        cls.validate_mapping(
            data=data,
            schema=schema,
        )

    @classmethod
    def validate_mapping(
        cls,
        *,
        data: Mapping[str, Any],
        schema: ValidationSchema,
    ) -> None:
        """
        Validate a mapping against a validation schema.
        """

        for field_name, rule in schema.items():
            cls._validate_field(
                field_name=field_name,
                value=data.get(field_name),
                rule=rule,
            )

    @classmethod
    def _validate_field(
        cls,
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if value is None:
            cls._validate_nullable(
                field_name=field_name,
                rule=rule,
            )
            return

        cls._validate_type(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_bool_rejection(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_non_empty(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_finite(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_numeric_bounds(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_items(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_mapping_items(
            field_name=field_name,
            value=value,
            rule=rule,
        )

    @staticmethod
    def _validate_nullable(
        *,
        field_name: str,
        rule: ValidationRule,
    ) -> None:
        if not rule.get(
            "nullable",
            False,
        ):
            raise TypeError(
                f"{field_name} cannot be None."
            )

    @staticmethod
    def _validate_type(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        expected_type = rule.get("type")

        if expected_type is None:
            return

        if not isinstance(
            value,
            expected_type,
        ):
            raise TypeError(
                f"{field_name} must be "
                f"{SchemaValidator._format_type_name(expected_type)}."
            )

    @staticmethod
    def _validate_bool_rejection(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if rule.get(
            "reject_bool",
            False,
        ) and isinstance(
            value,
            bool,
        ):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not rule.get(
            "non_empty",
            False,
        ):
            return

        checked_value = value

        if isinstance(
            checked_value,
            str,
        ) and rule.get(
            "strip",
            False,
        ):
            checked_value = checked_value.strip()

        if isinstance(
            checked_value,
            SIZED_TYPES,
        ) and len(checked_value) == 0:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not rule.get(
            "finite",
            False,
        ):
            return

        if isinstance(
            value,
            (int, float),
        ) and not isinstance(
            value,
            bool,
        ):
            if not math.isfinite(value):
                raise ValueError(
                    f"{field_name} must be finite."
                )

    @staticmethod
    def _validate_numeric_bounds(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not isinstance(
            value,
            (int, float),
        ) or isinstance(
            value,
            bool,
        ):
            return

        min_value = rule.get("min_value")
        max_value = rule.get("max_value")

        if min_value is not None and value < min_value:
            raise ValueError(
                f"{field_name} must be >= {min_value}."
            )

        if max_value is not None and value > max_value:
            raise ValueError(
                f"{field_name} must be <= {max_value}."
            )

        if rule.get(
            "non_negative",
            False,
        ) and value < 0:
            raise ValueError(
                f"{field_name} cannot be negative."
            )

    @classmethod
    def _validate_items(
        cls,
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not cls._has_item_rules(
            rule=rule,
        ):
            return

        if not isinstance(
            value,
            COLLECTION_TYPES,
        ):
            raise TypeError(
                f"{field_name} must be a collection."
            )

        cls._validate_item_types(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_non_empty_items(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_bool_items(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_finite_items(
            field_name=field_name,
            value=value,
            rule=rule,
        )
        cls._validate_item_numeric_bounds(
            field_name=field_name,
            value=value,
            rule=rule,
        )

    @staticmethod
    def _has_item_rules(
        *,
        rule: ValidationRule,
    ) -> bool:
        return any(
            (
                rule.get("item_type") is not None,
                rule.get("non_empty_items", False),
                rule.get("reject_bool_items", False),
                rule.get("finite_items", False),
                rule.get("min_item_value") is not None,
                rule.get("max_item_value") is not None,
            )
        )

    @staticmethod
    def _validate_item_types(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        item_type = rule.get("item_type")

        if item_type is None:
            return

        for item in value:
            if not isinstance(
                item,
                item_type,
            ):
                raise TypeError(
                    f"{field_name} items must be "
                    f"{SchemaValidator._format_type_name(item_type)}."
                )

    @staticmethod
    def _validate_non_empty_items(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not rule.get(
            "non_empty_items",
            False,
        ):
            return

        for item in value:
            checked_item = item

            if isinstance(
                checked_item,
                str,
            ) and rule.get(
                "strip",
                False,
            ):
                checked_item = checked_item.strip()

            if isinstance(
                checked_item,
                SIZED_TYPES,
            ) and len(checked_item) == 0:
                raise ValueError(
                    f"{field_name} items cannot be empty."
                )

    @staticmethod
    def _validate_bool_items(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not rule.get(
            "reject_bool_items",
            False,
        ):
            return

        for item in value:
            if isinstance(
                item,
                bool,
            ):
                raise TypeError(
                    f"{field_name} items cannot be bool."
                )

    @staticmethod
    def _validate_finite_items(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        if not rule.get(
            "finite_items",
            False,
        ):
            return

        for item in value:
            if isinstance(
                item,
                (int, float),
            ) and not isinstance(
                item,
                bool,
            ):
                if not math.isfinite(item):
                    raise ValueError(
                        f"{field_name} items must be finite."
                    )

    @staticmethod
    def _validate_item_numeric_bounds(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        min_item_value = rule.get("min_item_value")
        max_item_value = rule.get("max_item_value")

        if min_item_value is None and max_item_value is None:
            return

        for item in value:
            if not isinstance(
                item,
                (int, float),
            ) or isinstance(
                item,
                bool,
            ):
                continue

            if min_item_value is not None and item < min_item_value:
                raise ValueError(
                    f"{field_name} items must be >= {min_item_value}."
                )

            if max_item_value is not None and item > max_item_value:
                raise ValueError(
                    f"{field_name} items must be <= {max_item_value}."
                )

    @staticmethod
    def _validate_mapping_items(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
    ) -> None:
        key_type = rule.get("key_type")
        value_type = rule.get("value_type")

        if key_type is None and value_type is None:
            return

        if not isinstance(
            value,
            Mapping,
        ):
            raise TypeError(
                f"{field_name} must be a mapping."
            )

        for key, item_value in value.items():
            if key_type is not None and not isinstance(
                key,
                key_type,
            ):
                raise TypeError(
                    f"{field_name} keys must be "
                    f"{SchemaValidator._format_type_name(key_type)}."
                )

            if value_type is not None and not isinstance(
                item_value,
                value_type,
            ):
                raise TypeError(
                    f"{field_name} values must be "
                    f"{SchemaValidator._format_type_name(value_type)}."
                )

    @staticmethod
    def _format_type_name(
        expected_type: type | tuple[type, ...],
    ) -> str:
        if isinstance(
            expected_type,
            tuple,
        ):
            return " or ".join(
                SchemaValidator._format_type_name(item)
                for item in expected_type
            )

        return expected_type.__name__