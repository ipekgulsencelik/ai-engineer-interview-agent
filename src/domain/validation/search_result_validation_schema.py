from __future__ import annotations


SEARCH_RESULT_VALIDATION_SCHEMA = {
    "id": {
        "type": str,
    },
    "text": {
        "type": str,
    },
    "score": {
        "type": (int, float),
        "finite": True,
        "min_value": 0.0,
    },
}