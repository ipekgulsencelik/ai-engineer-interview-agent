from src.container import Container
from src.domain.entities.question import Question


def run() -> None:
    container = Container()

    service = container.build_follow_up_generation_service()

    question = Question(
        id="rag_001",
        text="What is Retrieval-Augmented Generation?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[
            "retrieval",
            "generation",
            "external knowledge",
            "vector database",
        ],
        keywords=[
            "rag",
            "retrieval",
            "llm",
        ],
    )

    result = service.generate(
        question=question,
        answer=("RAG combines retrieval with generation models."),
    )

    print("\n=== FOLLOW-UP RESULT ===\n")

    print(result)


if __name__ == "__main__":
    run()
