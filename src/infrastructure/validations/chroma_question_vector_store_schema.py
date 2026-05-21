from __future__ import annotations

from typing import Final

from src.domain.entities.question import Question
from src.infrastructure.constants.vector_store_limits import (
    MIN_TOP_K,
)
from src.infrastructure.validation.schema_types import (
    SchemaDefinition,
)


CHROMA_QUESTION_VECTOR_STORE_SCHEMA: Final[
    SchemaDefinition
] = {
    "questions": {
        "type": list,
        "allow_empty": False,
        "item_type": Question,
    },
    "embeddings": {
        "type": list,
        "allow_empty": False,
        "item_type": list,
    },
    "embedding": {
        "type": list,
        "allow_empty": False,
        "item_type": (int, float),
        "allow_bool": False,
    },
    "top_k": {
        "type": int,
        "min_value": MIN_TOP_K,
        "allow_bool": False,
    },
}