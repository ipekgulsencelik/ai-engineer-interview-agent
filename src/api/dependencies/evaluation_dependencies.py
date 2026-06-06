from __future__ import annotations

from fastapi import Depends

from src.api.app_state import (
    get_service_container,
)
from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.infrastructure.containers.service_container import (
    ServiceContainer,
)


def get_answer_evaluation_service(
    container: ServiceContainer = Depends(
        get_service_container,
    ),
) -> AnswerEvaluationService:
    """
    AnswerEvaluationService dependency provider.
    """

    return container.answer_evaluation_service