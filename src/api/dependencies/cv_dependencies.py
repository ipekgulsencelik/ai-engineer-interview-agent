from __future__ import annotations

from typing import Annotated, TypeAlias

from fastapi import Depends

from src.api.app_state import get_service_container
from src.application.services.cv_analysis_orchestration_service import (
    CVAnalysisOrchestrationService,
)
from src.infrastructure.containers.service_container import ServiceContainer


ServiceContainerDependency: TypeAlias = Annotated[
    ServiceContainer,
    Depends(get_service_container),
]


CVAnalysisOrchestrationServiceDependency: TypeAlias = Annotated[
    CVAnalysisOrchestrationService,
    Depends(get_cv_analysis_orchestration_service),
]


def get_cv_analysis_orchestration_service(
    container: ServiceContainerDependency,
) -> CVAnalysisOrchestrationService:
    """
    Resolve CVAnalysisOrchestrationService from the application service container.
    """

    return container.cv_analysis_orchestration_service