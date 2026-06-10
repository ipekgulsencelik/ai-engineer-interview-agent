from __future__ import annotations

from enum import StrEnum


class QuestionCategory(StrEnum):
    """
    AI Engineer interview question category enum.

    Değerler machine-readable snake_case tutulur.
    """
    
    ALGORITHMS = "algorithms"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"
    DEBUGGING = "debugging"
    BEHAVIORAL = "behavioral"
    SCENARIO = "scenario"   
    LLM_FUNDAMENTALS = "llm_fundamentals"
    PROMPT_ENGINEERING = "prompt_engineering"
    RAG = "rag"
    VECTOR_DATABASES = "vector_databases"
    EMBEDDING = "embedding"
    LANGCHAIN_AGENTS = "langchain_agents"
    AGENTS = "agents"
    EVALUATION = "evaluation"
    MLOPS = "mlops"
    FINE_TUNING = "fine_tuning"