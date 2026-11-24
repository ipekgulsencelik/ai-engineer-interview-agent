from __future__ import annotations

import os
from typing import Final

BASE_API_URL: Final[str] = os.environ.get(
    "INTERVIEW_API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

NEXT_QUESTION_ROUTE: Final[str] = (
    "/api/v1/retrieval/next-question"
)

EVALUATION_ROUTE: Final[str] = (
    "/api/v1/evaluations"
)

INTERVIEW_SESSIONS_ROUTE: Final[str] = (
    "/api/v1/interview/sessions"
)
