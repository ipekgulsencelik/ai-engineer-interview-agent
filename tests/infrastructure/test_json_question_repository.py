from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)


def test_json_question_repository_loads_questions() -> None:
    repository = JsonQuestionRepository(
        "data/questions.json",
    )

    questions = repository.list_all()

    assert len(questions) == 3


def test_json_question_repository_get_by_id() -> None:
    repository = JsonQuestionRepository(
        "data/questions.json",
    )

    question = repository.get_by_id(
        "rag_jr_001",
    )

    assert question is not None
    assert question.id == "rag_jr_001"


def test_json_question_repository_returns_none_for_unknown_id() -> None:
    repository = JsonQuestionRepository(
        "data/questions.json",
    )

    question = repository.get_by_id(
        "unknown_question",
    )

    assert question is None
