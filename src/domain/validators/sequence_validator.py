from __future__ import annotations

from typing import Any, Final

from src.domain.formatters.validation_formatter import (
    ValidationFormatter,
)
from src.domain.validation.schema_rules import (
    ValidationRule,
)
from src.domain.validation.validation_types import (
    ErrorFactory,
)


COLLECTION_TYPES: Final[tuple[type, ...]] = (
    list,
    tuple,
    set,
    frozenset,
)


class SequenceValidator:
    """
    Collection item validation utilities.
    """

    @staticmethod
    def validate(
        *,
        field_name: str,
        value: Any,
        rule: ValidationRule,
        error_factory: ErrorFactory,
    ) -> None:
        if rule.item_type is None:
            return

        if not isinstance(
            value,
            COLLECTION_TYPES,
        ):
            raise error_factory(
                f"{field_name} must be a collection."
            )

        for index, item in enumerate(value):
            if not isinstance(
                item,
                rule.item_type,
            ):
                raise error_factory(
                    f"{field_name}[{index}] must be "
                    f"{ValidationFormatter.format_type_name(rule.item_type)}."
                )

            if isinstance(item, str):
                normalized_item = (
                    item.strip()
                    if rule.strip_items
                    else item
                )

                if not normalized_item:
                    raise error_factory(
                        f"{field_name}[{index}] cannot be empty."
                    )