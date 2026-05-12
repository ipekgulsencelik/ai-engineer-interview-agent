from __future__ import annotations

from typing import Any


NON_NEGATIVE_INT = {
    "type": int,
    "nullable": True,
    "min_value": 0,
}

NON_NEGATIVE_FLOAT = {
    "type": (int, float),
    "nullable": True,
    "finite": True,
    "min_value": 0.0,
}


LLM_RESPONSE_METADATA_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "model": {
        "type": str,
        "nullable": True,
        "non_empty": True,
    },
    "prompt_tokens": NON_NEGATIVE_INT,
    "completion_tokens": NON_NEGATIVE_INT,
    "total_tokens": NON_NEGATIVE_INT,
    "latency_seconds": NON_NEGATIVE_FLOAT,
    "finish_reason": {
        "type": str,
        "nullable": True,
        "non_empty": True,
    },
    "raw_response": {
        "type": dict,
        "nullable": True,
    },
}