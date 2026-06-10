from __future__ import annotations

from typing import Annotated, TypeAlias

from fastapi import Depends

from src.api.app_state import get_service_container
from src.application.use_cases.run_interview_step_use_case import (
    RunInterviewStepUseCase,
)
from src.infrastructure.containers.service_container import ServiceContainer


ServiceContainerDependency: TypeAlias = Annotated[
    ServiceContainer,
    Depends(get_service_container),
]


def get_run_interview_step_use_case(
    container: ServiceContainerDependency,
) -> RunInterviewStepUseCase:
    """
    Resolve RunInterviewStepUseCase from the application service container.
    """

    return container.run_interview_step_use_case


RunInterviewStepUseCaseDependency: TypeAlias = Annotated[
    RunInterviewStepUseCase,
    Depends(get_run_interview_step_use_case),
]