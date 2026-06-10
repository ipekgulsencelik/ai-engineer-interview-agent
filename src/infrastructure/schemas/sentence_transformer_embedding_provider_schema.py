from __future__ import annotations

from typing import Any, Final


SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA: Final[
    dict[str, dict[str, Any]]
] = {
    "model_name": {
        "type": (str, type(None)),
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
        "min_value": 0,
        "allow_bool": False,
    },
    "retry_backoff_seconds": {
        "type": (int, float),
        "min_value": 0.0,
        "allow_bool": False,
    },
    "batch_size": {
        "type": int,
        "min_value": 1,
        "allow_bool": False,
    },
    "normalize_embeddings": {
        "type": bool,
    },
}