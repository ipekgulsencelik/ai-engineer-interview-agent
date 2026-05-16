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
from src.domain.errors.question_validation_error import (
    QuestionValidationError,
)
from src.application.factories.question_factory_builder import (
    QuestionFactoryBuilder,
)


def test_question_factory_should_create_question_from_payload() -> None:
    factory = QuestionFactoryBuilder.build_default()

    question = factory.create_from_payload(
        {
            "id": "rag_jr_001",
            "text": "What is RAG?",
            "category": "RAG",
            "level": "jr",
            "question_type": "conceptual",
            "difficulty": 3,
            "expected_points": [
                "retrieval",
                "generation",
            ],
            "keywords": [
                "rag",
                "retrieval",
            ],
            "followup": "What can go wrong in RAG?",
            "ideal_answer_hint": "RAG uses retrieved context.",
            "market_weight": 0.7,
            "followup_allowed": True,
        }
    )

    assert question.id == "rag_jr_001"
    assert question.text == "What is RAG?"

    assert question.category == QuestionCategory.RAG
    assert question.level == Level.JR
    assert question.question_type == QuestionType.CONCEPTUAL

    assert question.difficulty == 3

    assert question.expected_points == [
        "retrieval",
        "generation",
    ]

    assert question.keywords == [
        "rag",
        "retrieval",
    ]

    assert question.followup == "What can go wrong in RAG?"

    assert question.ideal_answer_hint == (
        "RAG uses retrieved context."
    )

    assert question.market_weight == 0.7
    assert question.followup_allowed is True


def test_question_factory_should_resolve_category_alias() -> None:
    factory = QuestionFactoryBuilder.build_default()

    question = factory.create_from_payload(
        {
            "id": "vector_mid_001",
            "text": (
                "How do vector databases support "
                "semantic search?"
            ),
            "category": "Vector DB",
            "level": "MID",
            "question_type": "conceptual",
            "difficulty": 3,
        }
    )

    assert question.category == (
        QuestionCategory.VECTOR_DATABASES
    )


def test_question_factory_missing_required_field_should_fail() -> None:
    factory = QuestionFactoryBuilder.build_default()

    with pytest.raises(
        QuestionValidationError,
    ):
        factory.create_from_payload(
            {
                "id": "q1",
                "text": "What is RAG?",
                "category": "RAG",
                "level": "JR",
                "difficulty": 3,
            }
        )


def test_question_factory_invalid_level_should_fail() -> None:
    factory = QuestionFactoryBuilder.build_default()

    with pytest.raises(
        EnumParsingError,
    ):
        factory.create_from_payload(
            {
                "id": "q1",
                "text": "What is RAG?",
                "category": "RAG",
                "level": "LEAD",
                "question_type": "conceptual",
                "difficulty": 3,
            }
        )


def test_question_factory_invalid_keyword_type_should_fail() -> None:
    factory = QuestionFactoryBuilder.build_default()

    with pytest.raises(
        QuestionValidationError,
    ):
        factory.create_from_payload(
            {
                "id": "q1",
                "text": "What is RAG?",
                "category": "RAG",
                "level": "JR",
                "question_type": "conceptual",
                "difficulty": 3,
                "keywords": [
                    "retrieval",
                    123,
                ],
            }
        )


def test_question_factory_invalid_followup_type_should_fail() -> None:
    factory = QuestionFactoryBuilder.build_default()

    with pytest.raises(
        QuestionValidationError,
    ):
        factory.create_from_payload(
            {
                "id": "q1",
                "text": "What is RAG?",
                "category": "RAG",
                "level": "JR",
                "question_type": "conceptual",
                "difficulty": 3,
                "followup": 123,
            }
        )