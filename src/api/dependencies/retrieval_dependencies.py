from __future__ import annotations

from typing import Annotated, TypeAlias

from fastapi import Depends

from src.api.app_state import get_service_container
from src.application.services.adaptive_question_selection_service import (
    AdaptiveQuestionSelectionService,
)
from src.infrastructure.containers.service_container import ServiceContainer


ServiceContainerDependency: TypeAlias = Annotated[
    ServiceContainer,
    Depends(get_service_container),
]


def get_adaptive_question_selection_service(
    container: ServiceContainerDependency,
) -> AdaptiveQuestionSelectionService:
    """
    Resolve AdaptiveQuestionSelectionService from the application service container.
    """

    return container.adaptive_selection_service


AdaptiveQuestionSelectionServiceDependency: TypeAlias = Annotated[
    AdaptiveQuestionSelectionService,
    Depends(get_adaptive_question_selection_service),
]