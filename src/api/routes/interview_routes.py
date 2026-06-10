from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from src.api.dependencies.interview_dependencies import (
    get_run_interview_step_use_case,
)
from src.api.mappers.interview_request_mapper import (
    InterviewRequestMapper,
)
from src.api.mappers.interview_step_response_mapper import (
    InterviewStepResponseMapper,
)
from src.api.schemas.interview.requests import (
    InterviewStepRequest,
)
from src.api.schemas.interview.responses import (
    InterviewStepResponse,
)
from src.application.use_cases.run_interview_step_use_case import (
    RunInterviewStepUseCase,
)


router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


@router.post(
    "/step",
    response_model=InterviewStepResponse,
)
def run_interview_step(
    request: InterviewStepRequest,
    use_case: RunInterviewStepUseCase = Depends(
        get_run_interview_step_use_case,
    ),
) -> InterviewStepResponse:
    """
    Adaptive interview orchestration endpoint.
    """

    payload = InterviewRequestMapper.to_payload(
        request=request,
    )

    result = use_case.execute(
        payload=payload,
    )

    return InterviewStepResponseMapper.from_result(
        result=result,
    )