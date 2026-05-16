from __future__ import annotations

from pathlib import Path
from typing import Any, Final


QUESTION_BANK_PATH_SCHEMA: Final[dict[str, dict[str, Any]]] = {
    "file_path": {
        "type": Path,
        "non_empty": True,
    },
}