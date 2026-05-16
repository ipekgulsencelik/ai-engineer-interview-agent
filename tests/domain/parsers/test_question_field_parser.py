from __future__ import annotations

import pytest

from src.domain.enums.level import Level
from src.domain.enums.question_category import (
    QuestionCategory,
)
from src.domain.enums.question_type import (
    QuestionType,
)
from src.domain.errors.enum_parsing_error import (
    EnumParsingError,
)
from src.domain.parsers.factories.question_field_parser_factory import (
    QuestionFieldParserFactory,
)


def test_parse_level_should_return_level_enum() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    result = parser.parse_level(" jr ")

    assert result == Level.JR


def test_parse_question_type_should_return_question_type_enum() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    result = parser.parse_question_type(
        "Coding",
    )

    assert result == QuestionType.CODING


def test_parse_question_type_should_normalize_hyphen() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    result = parser.parse_question_type(
        "system-design",
    )

    assert result == (
        QuestionType.SYSTEM_DESIGN
    )


def test_parse_category_should_return_category_enum() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    result = parser.parse_category(
        "RAG",
    )

    assert result == QuestionCategory.RAG


def test_parse_category_should_resolve_vector_db_alias() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    result = parser.parse_category(
        "Vector DB",
    )

    assert result == (
        QuestionCategory.VECTOR_DATABASES
    )


def test_parse_category_should_resolve_langchain_agents_alias() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    result = parser.parse_category(
        "LangChain & Agents",
    )

    assert result == (
        QuestionCategory.LANGCHAIN_AGENTS
    )


def test_invalid_level_should_raise_enum_parsing_error() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    with pytest.raises(EnumParsingError):
        parser.parse_level("lead")


def test_invalid_category_should_raise_enum_parsing_error() -> None:
    parser = (
        QuestionFieldParserFactory.create_default()
    )

    with pytest.raises(EnumParsingError):
        parser.parse_category("backend")