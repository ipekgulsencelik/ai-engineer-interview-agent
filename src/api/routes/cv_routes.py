from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from src.api.dependencies.cv_dependencies import (
    get_cv_analysis_orchestration_service,
)
from src.api.mappers.cv_analysis_response_mapper import (
    CVAnalysisResponseMapper,
)
from src.api.schemas.cv_analysis_response import (
    CVAnalysisResponse,
)
from src.api.storage.cv_upload_file_storage import (
    CVUploadFileStorage,
)
from src.application.services.cv_analysis_orchestration_service import (
    CVAnalysisOrchestrationService,
)


router = APIRouter(
    prefix="/cv",
    tags=["CV Analysis"],
)


@router.post(
    "/analyze",
    response_model=CVAnalysisResponse,
    summary="Analyze candidate CV",
)
async def analyze_cv(
    file: UploadFile = File(...),
    service: CVAnalysisOrchestrationService = Depends(
        get_cv_analysis_orchestration_service,
    ),
) -> CVAnalysisResponse:
    """
    End-to-end CV analysis endpoint.
    """

    try:
        temp_file_path = await CVUploadFileStorage.save_to_temp_file(
            file=file,
        )

        profile, gap_analysis = service.analyze_cv(
            file_path=temp_file_path,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return CVAnalysisResponseMapper.from_profile_and_gap_analysis(
        profile=profile,
        gap_analysis=gap_analysis,
    )