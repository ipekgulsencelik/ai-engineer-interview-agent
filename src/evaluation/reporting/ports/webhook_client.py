from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class WebhookClient(
    ABC,
):
    """
    Webhook delivery port.
    """

    @abstractmethod
    def post(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
    ) -> int | None:
        """
        Sends a webhook POST request.

        Returns HTTP status code when available.
        """