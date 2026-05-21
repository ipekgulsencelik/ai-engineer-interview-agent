from __future__ import annotations

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)


def _question() -> Question:
    return Question(
        id="rag_jr_001",
        text="What is Retrieval-Augmented Generation?",
        category=QuestionCategory.RAG,
        level=Level.JR,
        question_type=QuestionType.CONCEPTUAL,
        difficulty=3,
        expected_points=[
            "retrieval",
            "generation",
        ],
        market_weight=0.8,
    )


def test_question_search_result_creation_success() -> None:
    result = QuestionSearchResult(
        question=_question(),
        distance=0.25,
        score=0.75,
    )

    assert result.question.id == "rag_jr_001"
    assert result.distance == 0.25
    assert result.score == 0.75


def test_question_search_result_negative_distance_should_fail() -> None:
    with pytest.raises(ValueError):
        QuestionSearchResult(
            question=_question(),
            distance=-0.1,
            score=0.75,
        )


def test_question_search_result_score_out_of_range_should_fail() -> None:
    with pytest.raises(ValueError):
        QuestionSearchResult(
            question=_question(),
            distance=0.25,
            score=1.5,
        )


def test_question_search_result_bool_score_should_fail() -> None:
    with pytest.raises(TypeError):
        QuestionSearchResult(
            question=_question(),
            distance=0.25,
            score=True,  # type: ignore[arg-type]
        )