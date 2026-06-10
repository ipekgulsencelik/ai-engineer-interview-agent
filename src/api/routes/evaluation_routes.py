from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from src.api.dependencies.evaluation_dependencies import (
    get_answer_evaluation_service,
)
from src.api.mappers.evaluation_request_mapper import (
    EvaluationRequestMapper,
)
from src.api.mappers.evaluation_response_mapper import (
    EvaluationResponseMapper,
)
from src.api.schemas.evaluation.requests import (
    EvaluationRequest,
)
from src.api.schemas.evaluation.responses import (
    EvaluationResponse,
)
from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)


router = APIRouter(
    prefix="/evaluations",
    tags=["Evaluations"],
)


@router.post(
    "",
    response_model=EvaluationResponse,
    summary="Evaluate candidate answer",
)
def evaluate_answer(
    request: EvaluationRequest,
    service: AnswerEvaluationService = Depends(
        get_answer_evaluation_service,
    ),
) -> EvaluationResponse:
    """
    Candidate answer evaluation endpoint.
    """

    question = EvaluationRequestMapper.to_question(
        request=request,
    )

    result = service.evaluate(
        question=question,
        answer=request.answer,
    )

    return EvaluationResponseMapper.from_result(
        result=result,
    )