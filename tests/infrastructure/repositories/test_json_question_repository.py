from __future__ import annotations

from pathlib import Path

from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)


def test_json_question_repository_should_load_questions() -> None:
    repository = (
        JsonQuestionRepositoryBuilder.build_default(
            file_path=Path(
                "data/question_bank/questions.json"
            ),
        )
    )

    questions = repository.list_all()

    assert questions
    assert questions[0].id == "rag_jr_001"