from __future__ import annotations

from pathlib import Path


QUESTION_BANK_FALLBACK_PATHS: dict[str, Path] = {
    "data/questions.json": Path(
        "data/question_bank/questions.json"
    ),
}