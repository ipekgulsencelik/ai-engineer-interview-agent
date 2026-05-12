from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)


def run() -> None:
    repository = JsonQuestionRepository(
        "data/question_bank/questions.json",
    )

    questions = repository.list_all()

    print("\nLoaded Questions\n")

    for question in questions:
        print(
            f"{question.id} | "
            f"{question.category} | "
            f"{question.level}"
        )

    print("\nTotal Questions:", len(questions))

    question = repository.get_by_id(
        "rag_jr_001",
    )

    print("\nLookup Result:\n")

    print(question)


if __name__ == "__main__":
    run()