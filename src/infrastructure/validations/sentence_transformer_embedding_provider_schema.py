from __future__ import annotations

from typing import Final

from src.infrastructure.constants.validation_limits import (
    MIN_BATCH_SIZE,
    MIN_RETRY_BACKOFF_SECONDS,
    MIN_RETRY_COUNT,
)
from src.infrastructure.constants.validation_types import (
    NONE_TYPE,
)
from src.infrastructure.validation.schema_types import (
    SchemaDefinition,
)


SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA: Final[
    SchemaDefinition
] = {
    "model_name": {
        "type": (str, NONE_TYPE),
        "non_empty": True,
        "strip": True,
    },
    "text": {
        "type": str,
        "non_empty": True,
        "strip": True,
    },
    "texts": {
        "type": list,
        "allow_empty": False,
        "item_type": str,
        "strip_items": True,
    },
    "retry_count": {
        "type": int,
        "min_value": MIN_RETRY_COUNT,
        "allow_bool": False,
    },
    "retry_backoff_seconds": {
        "type": (int, float),
        "min_value": MIN_RETRY_BACKOFF_SECONDS,
        "allow_bool": False,
    },
    "batch_size": {
        "type": int,
        "min_value": MIN_BATCH_SIZE,
        "allow_bool": False,
    },
    "normalize_embeddings": {
        "type": bool,
    },
}