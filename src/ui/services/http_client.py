from __future__ import annotations

from typing import Any

import requests

from src.ui.exceptions.api_client_error import (
    APIClientError,
)
from src.ui.validators.api_response_validator import (
    APIResponseValidator,
)


class HTTPClient:
    """
    Thin HTTP client wrapper for Streamlit UI services.
    """

    _session = requests.Session()

    @classmethod
    def post_json(
        cls,
        *,
        url: str,
        payload: dict[str, Any],
        timeout: int,
    ) -> dict[str, Any]:
        try:
            response = cls._session.post(
                url,
                json=payload,
                timeout=timeout,
            )

            response.raise_for_status()

            return APIResponseValidator.validate_json_object(
                value=response.json(),
            )

        except requests.RequestException as exc:
            raise APIClientError(
                "API request failed.",
            ) from exc