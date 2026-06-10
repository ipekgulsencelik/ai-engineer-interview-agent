from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.infrastructure.errors.question_bank_file_error import (
    QuestionBankFileError,
)
from src.infrastructure.schemas.question_record_schema import (
    QUESTION_RECORD_SCHEMA,
)


class QuestionRecordValidator:
    """
    Raw JSON question record validation.

    Bu validator infrastructure boundary'de çalışır.

    Domain validation yapmaz.
    Enum parse etmez.
    Entity üretmez.
    """

    @classmethod
    def validate(
        cls,
        *,
        payload: Mapping[str, Any],
        index: int,
    ) -> None:
        cls._validate_payload_type(
            payload=payload,
            index=index,
        )

        cls._validate_index(
            index=index,
        )

        for field_name, rules in QUESTION_RECORD_SCHEMA.items():
            cls._validate_required_field(
                payload=payload,
                field_name=field_name,
                rules=rules,
                index=index,
            )

            if field_name not in payload:
                continue

            value = payload[field_name]

            cls._validate_field_type(
                field_name=field_name,
                value=value,
                rules=rules,
                index=index,
            )

            cls._validate_string_rules(
                field_name=field_name,
                value=value,
                rules=rules,
                index=index,
            )

            cls._validate_list_rules(
                field_name=field_name,
                value=value,
                rules=rules,
                index=index,
            )

    @classmethod
    def validate_many(
        cls,
        records: object,
    ) -> None:
        if not isinstance(records, list):
            raise QuestionBankFileError(
                "Question records must be a list."
            )

        for index, record in enumerate(records):
            cls.validate(
                payload=record,
                index=index,
            )

    @staticmethod
    def _validate_payload_type(
        *,
        payload: Mapping[str, Any],
        index: int,
    ) -> None:
        if not isinstance(payload, Mapping):
            raise QuestionBankFileError(
                f"Question payload at index {index} must be a mapping."
            )

    @staticmethod
    def _validate_index(
        *,
        index: int,
    ) -> None:
        if isinstance(index, bool) or not isinstance(index, int):
            raise QuestionBankFileError(
                "question record index must be an integer."
            )

        if index < 0:
            raise QuestionBankFileError(
                "question record index cannot be negative."
            )

    @staticmethod
    def _validate_required_field(
        *,
        payload: Mapping[str, Any],
        field_name: str,
        rules: Mapping[str, Any],
        index: int,
    ) -> None:
        if rules.get("required") is True and field_name not in payload:
            raise QuestionBankFileError(
                f"Missing required question field '{field_name}' "
                f"at index {index}."
            )

    @staticmethod
    def _validate_field_type(
        *,
        field_name: str,
        value: object,
        rules: Mapping[str, Any],
        index: int,
    ) -> None:
        expected_type = rules.get("type")

        if expected_type is None:
            return

        if rules.get("allow_bool") is False and isinstance(value, bool):
            raise QuestionBankFileError(
                f"{field_name} at index {index} must not be a boolean."
            )

        if not isinstance(value, expected_type):
            raise QuestionBankFileError(
                f"{field_name} at index {index} has invalid type."
            )

    @staticmethod
    def _validate_string_rules(
        *,
        field_name: str,
        value: object,
        rules: Mapping[str, Any],
        index: int,
    ) -> None:
        if not isinstance(value, str):
            return

        if rules.get("non_empty") is True and not value.strip():
            raise QuestionBankFileError(
                f"{field_name} at index {index} cannot be empty."
            )

    @staticmethod
    def _validate_list_rules(
        *,
        field_name: str,
        value: object,
        rules: Mapping[str, Any],
        index: int,
    ) -> None:
        if not isinstance(value, list):
            return

        if rules.get("allow_empty") is False and not value:
            raise QuestionBankFileError(
                f"{field_name} at index {index} cannot be empty."
            )

        item_type = rules.get("item_type")

        if item_type is None:
            return

        for item in value:
            if not isinstance(item, item_type):
                raise QuestionBankFileError(
                    f"{field_name} at index {index} must contain only "
                    f"{item_type.__name__} items."
                )

            if (
                isinstance(item, str)
                and rules.get("strip_items") is True
                and not item.strip()
            ):
                raise QuestionBankFileError(
                    f"{field_name} at index {index} cannot contain "
                    f"empty string items."
                )