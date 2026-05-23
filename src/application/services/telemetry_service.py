from __future__ import annotations

from src.application.observability.evaluation_trace import (
    EvaluationTrace,
)
from src.application.observability.interview_trace import (
    InterviewTrace,
)
from src.application.factories.telemetry_payload_factory import (
    TelemetryPayloadFactory,
)
from src.infrastructure.logging.logger_factory import (
    LoggerFactory,
)


class TelemetryService:
    """
    Structured observability logging service.
    """

    def __init__(
        self,
    ) -> None:
        self._logger = (
            LoggerFactory.create_logger(
                "telemetry",
            )
        )

    def log_interview_trace(
        self,
        *,
        trace: InterviewTrace,
    ) -> None:
        self._logger.info(
            "Interview retrieval completed.",
            extra=(
                TelemetryPayloadFactory
                .build_interview_payload(
                    trace=trace,
                )
            ),
        )

    def log_evaluation_trace(
        self,
        *,
        trace: EvaluationTrace,
    ) -> None:
        self._logger.info(
            "Answer evaluation completed.",
            extra=(
                TelemetryPayloadFactory
                .build_evaluation_payload(
                    trace=trace,
                )
            ),
        )