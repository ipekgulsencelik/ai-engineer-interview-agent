from __future__ import annotations

from typing import get_type_hints

from src.evaluation.ops.ports import (
    BlockingFailureCounting,
    CIBenchmarkPolicyEvaluation,
    CIBenchmarkPolicyInputValidation,
    CIBenchmarkPolicyResultBuilding,
    CIPolicyEvaluation,
    CurrentTimeProviding,
    EvaluationRunResultBuilding,
    QualityGateEvaluation,
    RunDurationCalculation,
    RunIdGeneration,
    RunSuccessEvaluation,
)
from src.evaluation.ops.ports import ci_benchmark_policy_ports
from src.evaluation.ops.ports import evaluation_run_orchestrator_ports


def test_ci_benchmark_policy_ports_should_export_protocol_contracts() -> None:
    assert (
        CIBenchmarkPolicyInputValidation.__name__ == "CIBenchmarkPolicyInputValidation"
    )
    assert QualityGateEvaluation.__name__ == "QualityGateEvaluation"
    assert BlockingFailureCounting.__name__ == "BlockingFailureCounting"
    assert CIPolicyEvaluation.__name__ == "CIPolicyEvaluation"
    assert CIBenchmarkPolicyResultBuilding.__name__ == "CIBenchmarkPolicyResultBuilding"


def test_evaluation_run_orchestrator_ports_should_export_protocol_contracts() -> None:
    assert CIBenchmarkPolicyEvaluation.__name__ == "CIBenchmarkPolicyEvaluation"
    assert RunIdGeneration.__name__ == "RunIdGeneration"
    assert CurrentTimeProviding.__name__ == "CurrentTimeProviding"
    assert RunDurationCalculation.__name__ == "RunDurationCalculation"
    assert RunSuccessEvaluation.__name__ == "RunSuccessEvaluation"
    assert EvaluationRunResultBuilding.__name__ == "EvaluationRunResultBuilding"


def test_ci_benchmark_policy_ports_should_keep_expected_method_names() -> None:
    assert hasattr(CIBenchmarkPolicyInputValidation, "validate")
    assert hasattr(QualityGateEvaluation, "evaluate")
    assert hasattr(BlockingFailureCounting, "count")
    assert hasattr(CIPolicyEvaluation, "evaluate")
    assert hasattr(CIBenchmarkPolicyResultBuilding, "build")


def test_evaluation_run_orchestrator_ports_should_keep_expected_method_names() -> None:
    assert hasattr(CIBenchmarkPolicyEvaluation, "evaluate")
    assert hasattr(RunIdGeneration, "generate")
    assert hasattr(CurrentTimeProviding, "now")
    assert hasattr(RunDurationCalculation, "calculate")
    assert hasattr(RunSuccessEvaluation, "evaluate")
    assert hasattr(EvaluationRunResultBuilding, "build")


def test_ports_modules_should_define_precise_type_hints() -> None:
    ci_hints = get_type_hints(
        ci_benchmark_policy_ports.CIPolicyEvaluation.evaluate,
    )
    run_id_hints = get_type_hints(
        evaluation_run_orchestrator_ports.RunIdGeneration.generate,
    )

    assert ci_hints["blocking_failure_count"] is int
    assert ci_hints["return"] is bool
    assert run_id_hints["return"] is str
