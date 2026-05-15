from __future__ import annotations

from fastapi import Depends

from src.api.app_state import get_service_container
from src.application.use_cases.run_interview_step_use_case import (
    RunInterviewStepUseCase,
)
from src.infrastructure.containers.service_container import ServiceContainer


def get_run_interview_step_use_case(
    container: ServiceContainer = Depends(
        get_service_container,
    ),
) -> RunInterviewStepUseCase:
    """
    RunInterviewStepUseCase dependency provider.
    """

    return container.run_interview_step_use_case