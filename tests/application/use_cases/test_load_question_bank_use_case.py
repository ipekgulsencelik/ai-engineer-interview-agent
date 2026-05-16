from __future__ import annotations

from pathlib import Path

from src.application.use_cases.load_questions_use_case import (
    LoadQuestionsUseCase,
)
from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)


def test_load_questions_use_case_should_return_questions() -> None:
    repository = (
        JsonQuestionRepositoryBuilder.build_default(
            file_path=Path(
                "data/question_bank/questions.json"
            ),
        )
    )

    use_case = LoadQuestionsUseCase(
        question_repository=repository,
    )

    questions = use_case.execute()

    assert questions
    assert questions[0].id == "rag_jr_001"