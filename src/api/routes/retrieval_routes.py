from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from src.api.dependencies.retrieval_dependencies import (
    get_adaptive_question_selection_service,
)
from src.api.mappers.interview_question_response_mapper import (
    InterviewQuestionResponseMapper,
)
from src.api.schemas.interview.responses import (
    InterviewQuestionResponse,
)
from src.api.schemas.retrieval.question_retrieval_request import (
    QuestionRetrievalRequest,
)
from src.application.services.adaptive_question_selection_service import (
    AdaptiveQuestionSelectionService,
)
from src.domain.enums.level import (
    Level,
)
from src.domain.value_objects.interview_state import (
    InterviewState,
)


router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.post(
    "/next-question",
    response_model=InterviewQuestionResponse,
)
def next_question(
    request: QuestionRetrievalRequest,
    service: AdaptiveQuestionSelectionService = Depends(
        get_adaptive_question_selection_service,
    ),
) -> InterviewQuestionResponse:
    """
    Adaptive semantic interview retrieval endpoint.
    """

    state = InterviewState(
        current_level=Level(
            request.current_level.value,
        ),
    )

    try:
        result = service.select_next_question(
            query=request.query,
            state=state,
            top_k=request.top_k,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return (
        InterviewQuestionResponseMapper
        .from_selection_result(
            result=result,
        )
    )