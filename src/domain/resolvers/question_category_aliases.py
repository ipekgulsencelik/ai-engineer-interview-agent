from __future__ import annotations

from src.domain.enums.question_category import (
    QuestionCategory,
)


QUESTION_CATEGORY_ALIASES: dict[str, str] = {
    "vector_db": (
        QuestionCategory.VECTOR_DATABASES.value
    ),
    "vector_database": (
        QuestionCategory.VECTOR_DATABASES.value
    ),
    "vector_databases": (
        QuestionCategory.VECTOR_DATABASES.value
    ),

    "embedding": (
        QuestionCategory.EMBEDDING.value
    ),
    "embeddings": (
        QuestionCategory.EMBEDDING.value
    ),

    "llm_eval": (
        QuestionCategory.EVALUATION.value
    ),
    "evaluation": (
        QuestionCategory.EVALUATION.value
    ),
    "model_evaluation": (
        QuestionCategory.EVALUATION.value
    ),

    "rag": (
        QuestionCategory.RAG.value
    ),

    "agents": (
        QuestionCategory.AGENTS.value
    ),
    
    "langchain_agents": (
        QuestionCategory.LANGCHAIN_AGENTS.value
    ),

    "langchain_and_agents": (
        QuestionCategory.LANGCHAIN_AGENTS.value
    ),

    "langchain_agent": (
        QuestionCategory.LANGCHAIN_AGENTS.value
    ),

    "mlops": (
        QuestionCategory.MLOPS.value
    ),
}