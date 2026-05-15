from src.domain.entities.question import Question
from src.infrastructure.evaluator.groq_rubric_evaluator import (
    GroqRubricEvaluator,
)


def run() -> None:
    evaluator = GroqRubricEvaluator()

    question = Question(
        id="rag_jr_001",
        text="What is Retrieval-Augmented Generation?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[
            "retrieval",
            "generation",
            "external knowledge",
        ],
        keywords=["rag", "retrieval", "llm"],
    )

    result = evaluator.evaluate(
        question=question,
        answer="RAG combines retrieval systems with language generation models.",
    )

    print(result)


if __name__ == "__main__":
    run()
