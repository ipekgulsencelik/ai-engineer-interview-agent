from __future__ import annotations

from typing import Any, Final


QUESTION_LOOKUP_SCHEMA: Final[dict[str, dict[str, Any]]] = {
    "question_id": {
        "type": str,
        "non_empty": True,
        "strip": True,
    },
}