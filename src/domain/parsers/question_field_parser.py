from __future__ import annotations

from enum import Enum
from typing import Callable, TypeVar

from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType

EnumT = TypeVar(
    "EnumT",
    bound=Enum,
)


class QuestionFieldParser:
    """
    Raw external input değerlerini domain-safe enum değerlerine dönüştürür.

    Bu parser:
        - JSON
        - test fixture
        - seed data
        - API payload
        - repository output

    gibi kaynaklardan gelen string değerleri normalize eder.
    """

    @classmethod
    def parse_level(
        cls,
        value: Level | str,
    ) -> Level:
        return cls._parse_enum(
            value=value,
            enum_class=Level,
            field_name="level",
            normalize=lambda item: item.strip().upper(),
        )

    @classmethod
    def parse_question_type(
        cls,
        value: QuestionType | str,
    ) -> QuestionType:
        return cls._parse_enum(
            value=value,
            enum_class=QuestionType,
            field_name="question_type",
            normalize=lambda item: item.strip().lower(),
        )

    @classmethod
    def parse_category(
        cls,
        value: QuestionCategory | str,
    ) -> QuestionCategory:
        return cls._parse_enum(
            value=value,
            enum_class=QuestionCategory,
            field_name="category",
            normalize=cls._normalize_category,
        )

    @staticmethod
    def _normalize_category(
        value: str,
    ) -> str:
        normalized = " ".join(
            value.strip().split()
        )

        normalized = normalized.lower()

        normalized = normalized.replace(
            " & ",
            "_and_",
        )

        normalized = normalized.replace(
            "-",
            "_",
        )

        normalized = normalized.replace(
            " ",
            "_",
        )

        return normalized

    @staticmethod
    def _parse_enum(
        *,
        value: EnumT | str,
        enum_class: type[EnumT],
        field_name: str,
        normalize: Callable[[str], str],
    ) -> EnumT:
        if isinstance(value, enum_class):
            return value

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string or "
                f"{enum_class.__name__}."
            )

        normalized_value = normalize(value)

        try:
            return enum_class(normalized_value)

        except ValueError as error:
            allowed_values = [
                item.value
                for item in enum_class
            ]

            raise ValueError(
                f"Invalid {field_name}: {value}. "
                f"Expected one of: {allowed_values}"
            ) from error