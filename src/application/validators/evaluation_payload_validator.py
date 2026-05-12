from __future__ import annotations

import math
from dataclasses import fields, is_dataclass
from typing import Any


class EvaluationPayloadValidator:
    """
    EvaluationPayload schema validation kurallarını yönetir.
    """

    @classmethod
    def validate(
        cls,
        payload: object,
    ) -> None:
        if not is_dataclass(payload):
            raise TypeError(
                "payload must be a dataclass instance."
            )

        if payload.__class__.__name__ != "EvaluationPayload":
            raise TypeError(
                "payload must be an EvaluationPayload."
            )

        for field_info in fields(payload):
            value = getattr(
                payload,
                field_info.name,
            )

            metadata = dict(
                field_info.metadata,
            )

            cls._validate_nullable(
                field_name=field_info.name,
                value=value,
                metadata=metadata,
            )

            if value is None:
                continue

            cls._validate_type(
                field_name=field_info.name,
                value=value,
                metadata=metadata,
            )

            cls._validate_finite(
                field_name=field_info.name,
                value=value,
                metadata=metadata,
            )

            cls._validate_string_rules(
                field_name=field_info.name,
                value=value,
                metadata=metadata,
            )

            cls._validate_tuple_items(
                field_name=field_info.name,
                value=value,
                metadata=metadata,
            )

    @staticmethod
    def _validate_nullable(
        *,
        field_name: str,
        value: Any,
        metadata: dict[str, Any],
    ) -> None:
        nullable = metadata.get(
            "nullable",
            False,
        )

        if value is None and not nullable:
            raise ValueError(
                f"{field_name} cannot be None."
            )

    @staticmethod
    def _validate_type(
        *,
        field_name: str,
        value: Any,
        metadata: dict[str, Any],
    ) -> None:
        expected_type = metadata.get(
            "type",
        )

        if expected_type is None:
            return

        if isinstance(value, bool):
            raise TypeError(
                f"{field_name} cannot be boolean."
            )

        if not isinstance(
            value,
            expected_type,
        ):
            raise TypeError(
                f"{field_name} must be {expected_type}."
            )

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: Any,
        metadata: dict[str, Any],
    ) -> None:
        if not metadata.get(
            "finite",
            False,
        ):
            return

        if not math.isfinite(
            float(value),
        ):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_string_rules(
        *,
        field_name: str,
        value: Any,
        metadata: dict[str, Any],
    ) -> None:
        if not isinstance(
            value,
            str,
        ):
            return

        if metadata.get(
            "strip",
            False,
        ):
            if value != value.strip():
                raise ValueError(
                    f"{field_name} must be stripped."
                )

        if metadata.get(
            "non_empty",
            False,
        ):
            if not value.strip():
                raise ValueError(
                    f"{field_name} cannot be empty."
                )

    @staticmethod
    def _validate_tuple_items(
        *,
        field_name: str,
        value: Any,
        metadata: dict[str, Any],
    ) -> None:
        item_type = metadata.get(
            "item_type",
        )

        if item_type is None:
            return

        if not isinstance(
            value,
            tuple,
        ):
            raise TypeError(
                f"{field_name} must be tuple."
            )

        for item in value:
            if not isinstance(
                item,
                item_type,
            ):
                raise TypeError(
                    f"{field_name} items must be {item_type}."
                )

            if isinstance(
                item,
                str,
            ):
                if not item.strip():
                    raise ValueError(
                        f"{field_name} items cannot be empty."
                    )