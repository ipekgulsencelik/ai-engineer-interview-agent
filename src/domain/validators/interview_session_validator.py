from __future__ import annotations

import math
from dataclasses import fields
from datetime import datetime
from typing import TYPE_CHECKING

from src.domain.constants.validation_messages import (
    ERR_BOOL_FIELD,
    ERR_BOOL_ITEM,
    ERR_EMPTY,
    ERR_FIELD_TYPE,
    ERR_ITEM_FINITE,
    ERR_ITEM_MAX,
    ERR_ITEM_MIN,
    ERR_ITEM_NUMERIC,
    ERR_ITEM_TYPE,
    ERR_SESSION_TYPE,
    ERR_TZ_AWARE,
)
from src.domain.validation.interview_session_validation_schema import (
    FieldRule,
    INTERVIEW_SESSION_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.interview.interview_session import InterviewSession


class InterviewSessionValidator:
    """
    InterviewSession domain invariant validation.
    """

    @classmethod
    def validate(cls, session: "InterviewSession") -> None:
        cls._validate_model_type(session)

        for model_field in fields(session):
            field_name = model_field.name
            value = getattr(session, field_name)
            rules: FieldRule = INTERVIEW_SESSION_VALIDATION_SCHEMA.get(field_name, {})

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

            if rules.get("non_empty", False):
                cls._validate_non_empty_string(
                    field_name=field_name,
                    value=value,
                )

            if "item_type" in rules:
                cls._validate_collection_items(
                    field_name=field_name,
                    value=value,
                    item_type=rules["item_type"],
                    rules=rules,
                )

            if rules.get("timezone_aware", False):
                cls._validate_timezone_aware_datetime(
                    field_name=field_name,
                    value=value,
                )

    @staticmethod
    def _validate_model_type(session: "InterviewSession") -> None:
        from src.domain.interview.interview_session import InterviewSession

        if not isinstance(session, InterviewSession):
            raise TypeError(ERR_SESSION_TYPE)

        
    @staticmethod    
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        expected_type: type | tuple[type, ...] | None,
    ) -> None:
        if expected_type is None:
            return

        if expected_type is not bool and isinstance(value, bool):
            raise TypeError(ERR_BOOL_FIELD.format(field_name=field_name))

        if not isinstance(value, expected_type):
            raise TypeError(
                ERR_FIELD_TYPE.format(
                    field_name=field_name,
                    expected_type=expected_type,
                )
            )


    @staticmethod
    def _validate_non_empty_string(
        *,
        field_name: str,
        value: str,
    ) -> None:
        if not value.strip():
            raise ValueError(ERR_EMPTY.format(field_name=field_name))


    @classmethod
    def _validate_collection_items(
        cls,
        *,
        field_name: str,
        value: tuple[object, ...],
        item_type: type | tuple[type, ...],
        rules: FieldRule,
    ) -> None:
        for item in value:
            cls._validate_item_type(
                field_name=field_name,
                item=item,
                item_type=item_type,
            )

            if item_type is str:
                cls._validate_non_empty_string(
                    field_name=field_name,
                    value=item,  # type: ignore[arg-type]
                )

            if rules.get("finite", False) or "min_value" in rules or "max_value" in rules:
                cls._validate_numeric_item(
                    field_name=field_name,
                    item=item,
                    rules=rules,
                )


    @staticmethod
    def _validate_item_type(
        *,
        field_name: str,
        item: object,
        item_type: type | tuple[type, ...],
    ) -> None:
        if item_type is not bool and isinstance(item, bool):
            raise TypeError(ERR_BOOL_ITEM.format(field_name=field_name))

        if not isinstance(item, item_type):
            raise TypeError(
                ERR_ITEM_TYPE.format(
                    field_name=field_name,
                    item_type=item_type,
                )
            )
                

    @staticmethod
    def _validate_numeric_item(
        *,
        field_name: str,
        item: object,
        rules: FieldRule,
    ) -> None:
        if not isinstance(item, (int, float)) or isinstance(item, bool):
            raise TypeError(ERR_ITEM_NUMERIC.format(field_name=field_name))

        numeric_value = float(item)

        if rules.get("finite", False) and not math.isfinite(numeric_value):
            raise ValueError(ERR_ITEM_FINITE.format(field_name=field_name))

        min_value = rules.get("min_value")
        if min_value is not None and numeric_value < min_value:
            raise ValueError(
                ERR_ITEM_MIN.format(
                    field_name=field_name,
                    min_value=min_value,
                )
            )

        max_value = rules.get("max_value")
        if max_value is not None and numeric_value > max_value:
            raise ValueError(
                ERR_ITEM_MAX.format(
                    field_name=field_name,
                    max_value=max_value,
                )
            )

    @staticmethod
    def _validate_timezone_aware_datetime(
        *,
        field_name: str,
        value: datetime,
    ) -> None:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(ERR_TZ_AWARE.format(field_name=field_name))