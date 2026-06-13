from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.mappers.evaluation_dashboard_response_mapper import (
    EvaluationDashboardResponseMapper,
)
from src.api.schemas.evaluation.evaluation_dashboard_response import (
    EvaluationDashboardResponse,
)
from src.infrastructure.containers.service_container import (
    ServiceContainer,
)


router = APIRouter(
    prefix="/evaluation/dashboard",
    tags=["Evaluation Dashboard"],
)


def get_service_container() -> ServiceContainer:
    return ServiceContainer()


@router.get(
    "/{benchmark_id}/{benchmark_version}",
    response_model=EvaluationDashboardResponse,
)
def get_evaluation_dashboard(
    benchmark_id: str,
    benchmark_version: str,
    container: ServiceContainer = Depends(
        get_service_container,
    ),
) -> EvaluationDashboardResponse:
    dashboard = (
        container.evaluation_ops.evaluation_dashboard_query_service.get_dashboard(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
        )
    )

    return EvaluationDashboardResponseMapper.to_response(
        dashboard=dashboard,
    )