from __future__ import annotations


class WebhookDeliveryStatusEvaluator:
    """
    Evaluates webhook HTTP status codes.
    """

    def is_success(
        self,
        *,
        status_code: int | None,
    ) -> bool:
        if status_code is None:
            return True

        return 200 <= status_code < 300

    def error_message(
        self,
        *,
        status_code: int | None,
    ) -> str | None:
        if self.is_success(
            status_code=status_code,
        ):
            return None

        return (
            "webhook delivery failed "
            f"with status_code={status_code}"
        )