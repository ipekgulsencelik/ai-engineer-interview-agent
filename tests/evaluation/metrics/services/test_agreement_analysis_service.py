from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.services.agreement_analysis_service import (
    AgreementAnalysisService,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)


class StubCohensKappaCalculator:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def calculate(
        self,
        *,
        metric_name: str,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
        p_value: float | None = None,
        notes: str | None = None,
    ) -> AgreementResult:
        self.calls.append(
            {
                "metric_name": metric_name,
                "evaluator_a_labels": evaluator_a_labels,
                "evaluator_b_labels": evaluator_b_labels,
                "p_value": p_value,
                "notes": notes,
            }
        )
        return AgreementResult(
            metric_name=metric_name,
            kappa_score=1.0,
            agreement_ratio=1.0,
            sample_count=len(evaluator_a_labels),
            evaluator_count=2,
            method="cohen_kappa",
            is_reliable=True,
            interpretation="very_strong",
            p_value=p_value,
            notes=notes,
        )


def test_agreement_analysis_service_should_delegate_to_cohen_calculator() -> None:
    calculator = StubCohensKappaCalculator()
    service = AgreementAnalysisService(
        cohen_kappa_calculator=calculator,  # type: ignore[arg-type]
    )

    result = service.analyze_cohen_kappa(
        metric_name="overall_label",
        evaluator_a_labels=("pass", "fail"),
        evaluator_b_labels=("pass", "fail"),
        p_value=0.01,
        notes="delegated",
    )

    assert result.kappa_score == 1.0
    assert calculator.calls == [
        {
            "metric_name": "overall_label",
            "evaluator_a_labels": ("pass", "fail"),
            "evaluator_b_labels": ("pass", "fail"),
            "p_value": 0.01,
            "notes": "delegated",
        }
    ]
