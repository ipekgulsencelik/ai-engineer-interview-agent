from __future__ import annotations

import pytest

from src.evaluation.ops.repositories.audit_trail_repository import AuditTrailRepository
from src.evaluation.ops.repositories.dashboard_repository import DashboardRepository
from src.evaluation.ops.repositories.evaluation_run_read_repository import (
    EvaluationRunReadRepository,
)
from src.evaluation.ops.repositories.evaluation_run_write_repository import (
    EvaluationRunWriteRepository,
)


@pytest.mark.parametrize(
    ("repository_class", "abstract_methods"),
    [
        (AuditTrailRepository, {"save", "find_by_run_id"}),
        (DashboardRepository, {"load_dashboard"}),
        (
            EvaluationRunReadRepository,
            {
                "find_by_run_id",
                "find_by_experiment_id",
                "find_by_benchmark_id",
                "list_recent",
            },
        ),
        (EvaluationRunWriteRepository, {"save"}),
    ],
)
def test_repository_contracts_should_declare_expected_abstract_methods(
    repository_class: type[object],
    abstract_methods: set[str],
) -> None:
    assert repository_class.__abstractmethods__ == abstract_methods


@pytest.mark.parametrize(
    "repository_class",
    [
        AuditTrailRepository,
        DashboardRepository,
        EvaluationRunReadRepository,
        EvaluationRunWriteRepository,
    ],
)
def test_repository_contracts_should_not_be_instantiable(
    repository_class: type[object],
) -> None:
    with pytest.raises(TypeError):
        repository_class()
