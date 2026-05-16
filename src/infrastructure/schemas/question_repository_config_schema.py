from __future__ import annotations

from pathlib import Path
from typing import Any, Final


QUESTION_REPOSITORY_CONFIG_SCHEMA: Final[dict[str, dict[str, Any]]] = {
    "file_path": {
        "type": (str, Path),
        "non_empty": True,
        "strip": True,
    },
}