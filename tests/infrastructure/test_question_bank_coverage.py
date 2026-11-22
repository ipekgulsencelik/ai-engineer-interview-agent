"""Contract tests for the shipped question bank (data/question_bank/questions.json).

The bank must cover every interview category at every level, and every record
must load through the production mapper so the app never starts with a broken
or lopsided bank.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.infrastructure.mappers.question_mapper import QuestionMapper

BANK_PATH = Path(__file__).resolve().parents[2] / "data/question_bank/questions.json"

INTERVIEW_CATEGORIES = (
    QuestionCategory.LLM_FUNDAMENTALS,
    QuestionCategory.PROMPT_ENGINEERING,
    QuestionCategory.RAG,
    QuestionCategory.VECTOR_DATABASES,
    QuestionCategory.LANGCHAIN_AGENTS,
    QuestionCategory.MLOPS,
    QuestionCategory.EVALUATION,
    QuestionCategory.FINE_TUNING,
)
MIN_QUESTIONS_PER_CELL = 3


@pytest.fixture(scope="module")
def records() -> list[dict]:
    return json.loads(BANK_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def questions(records: list[dict]):
    mapper = QuestionMapper()
    return [
        mapper.from_mapping(payload=record, index=index)
        for index, record in enumerate(records)
    ]


def test_every_record_loads_through_production_mapper(questions, records) -> None:
    assert len(questions) == len(records)


def test_question_ids_are_unique(questions) -> None:
    ids = [question.id for question in questions]
    duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
    assert not duplicates


@pytest.mark.parametrize("category", INTERVIEW_CATEGORIES)
@pytest.mark.parametrize("level", list(Level))
def test_each_category_level_cell_is_covered(questions, category, level) -> None:
    count = sum(
        1
        for question in questions
        if question.category == category and question.level == level
    )
    assert count >= MIN_QUESTIONS_PER_CELL, (
        f"{category}/{level} has {count} questions; "
        f"need at least {MIN_QUESTIONS_PER_CELL}"
    )


def test_every_question_is_gradable(questions) -> None:
    """The evaluator and follow-up flow need rubric anchors on each question."""
    for question in questions:
        assert len(question.expected_points) >= 3, question.id
        assert question.keywords, question.id
        assert question.ideal_answer_hint, question.id
        assert question.followup, question.id


def test_difficulty_increases_with_level(questions) -> None:
    by_level: dict[Level, set[int]] = {}
    for question in questions:
        by_level.setdefault(question.level, set()).add(question.difficulty)
    assert max(by_level[Level.JR]) < min(by_level[Level.MID])
    assert max(by_level[Level.MID]) < min(by_level[Level.SENIOR])
