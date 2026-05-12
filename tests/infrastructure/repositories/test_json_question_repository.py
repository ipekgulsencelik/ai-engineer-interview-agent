import json
import pytest

from src.domain.entities.question import Question
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)

from pathlib import Path
from typing import Any


def write_json(
    path: Path,
    payload: Any,
) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file)


def build_valid_payload() -> list[dict]:
    return [
        {
            "id": "rag_jr_001",
            "text": "What is RAG?",
            "category": "rag",
            "level": "JR",
            "difficulty": 1,
            "question_type": "conceptual",
            "expected_points": [
                "retrieval",
            ],
            "keywords": [
                "rag",
            ],
            "market_weight": 0.9,
            "followup_allowed": True,
        }
    ]


def test_list_all_returns_question_entities(
    tmp_path,
) -> None:
    json_path = tmp_path / "questions.json"

    write_json(
        json_path,
        build_valid_payload(),
    )

    repository = JsonQuestionRepository(
        json_path,
    )

    questions = repository.list_all()

    assert len(questions) == 1
    assert isinstance(
        questions[0],
        Question,
    )


def test_get_by_id_returns_question(
    tmp_path,
) -> None:
    json_path = tmp_path / "questions.json"

    write_json(
        json_path,
        build_valid_payload(),
    )

    repository = JsonQuestionRepository(
        json_path,
    )

    question = repository.get_by_id(
        "rag_jr_001",
    )

    assert question is not None
    assert question.id == "rag_jr_001"


def test_get_by_id_returns_none_for_unknown_id(
    tmp_path,
) -> None:
    json_path = tmp_path / "questions.json"

    write_json(
        json_path,
        build_valid_payload(),
    )

    repository = JsonQuestionRepository(
        json_path,
    )

    question = repository.get_by_id(
        "unknown",
    )

    assert question is None


def test_repository_raises_error_for_duplicate_ids(
    tmp_path,
) -> None:
    json_path = tmp_path / "questions.json"

    payload = build_valid_payload() * 2

    write_json(
        json_path,
        payload,
    )

    repository = JsonQuestionRepository(
        json_path,
    )

    with pytest.raises(
        ValueError,
        match="Duplicate question ids found",
    ):
        repository.list_all()


def test_repository_raises_error_for_invalid_root(
    tmp_path,
) -> None:
    json_path = tmp_path / "questions.json"

    write_json(
        json_path,
        {
            "invalid": True,
        },
    )

    repository = JsonQuestionRepository(
        json_path,
    )

    with pytest.raises(
        ValueError,
        match="Question bank JSON root must be a list",
    ):
        repository.list_all()


def test_repository_raises_error_for_missing_required_fields(
    tmp_path,
) -> None:
    json_path = tmp_path / "questions.json"

    payload = [
        {
            "id": "q1",
        }
    ]

    write_json(
        json_path,
        payload,
    )

    repository = JsonQuestionRepository(
        json_path,
    )

    with pytest.raises(
        ValueError,
        match="missing required fields",
    ):
        repository.list_all()