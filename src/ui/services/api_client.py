from __future__ import annotations

from typing import Any

from src.ui.constants.api_routes import (
    BASE_API_URL,
    EVALUATION_ROUTE,
    NEXT_QUESTION_ROUTE,
)
from src.ui.constants.api_timeouts import (
    EVALUATION_TIMEOUT_SECONDS,
    NEXT_QUESTION_TIMEOUT_SECONDS,
)
from src.ui.services.http_client import (
    HTTPClient,
)


class APIClient:
    """
    Streamlit frontend API client.

    Bu sınıf:
        - UI endpoint orchestration yapar
        - endpoint-specific payload oluşturur
        - HTTP implementation detaylarını gizler
    """

    @classmethod
    def get_next_question(
        cls,
        *,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        return HTTPClient.post_json(
            url=f"{BASE_API_URL}{NEXT_QUESTION_ROUTE}",
            payload={
                "query": query,
                "top_k": top_k,
            },
            timeout=NEXT_QUESTION_TIMEOUT_SECONDS,
        )

    @classmethod
    def evaluate_answer(
        cls,
        *,
        question_id: str,
        answer: str,
    ) -> dict[str, Any]:
        return HTTPClient.post_json(
            url=f"{BASE_API_URL}{EVALUATION_ROUTE}",
            payload={
                "question_id": question_id,
                "answer": answer,
            },
            timeout=EVALUATION_TIMEOUT_SECONDS,
        )