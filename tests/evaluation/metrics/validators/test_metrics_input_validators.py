from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.validators.agreement_input_validator import (
    AgreementInputValidator,
)
from src.evaluation.metrics.validators.bootstrap_sampling_input_validator import (
    BootstrapSamplingInputValidator,
)
from src.evaluation.metrics.validators.category_metrics_input_validator import (
    CategoryMetricsInputValidator,
)
from src.evaluation.metrics.validators.correlation_input_validator import (
    CorrelationInputValidator,
)
from src.evaluation.metrics.validators.evaluator_alignment_input_validator import (
    EvaluatorAlignmentInputValidator,
)
from src.evaluation.metrics.validators.fleiss_kappa_input_validator import (
    FleissKappaInputValidator,
)
from src.evaluation.metrics.validators.regression_input_validator import (
    RegressionInputValidator,
)
from tests.evaluation.metrics.calculators.test_benchmark_aggregate_statistics_calculator import (
    _snapshot,
)
from src.evaluation.metrics.validators.benchmark_aggregation_input_validator import (
    BenchmarkAggregationInputValidator,
)
from src.evaluation.metrics.validators.trend_visualization_input_validator import (
    TrendVisualizationInputValidator,
)


def test_sequence_input_validators_should_accept_valid_inputs() -> None:
    AgreementInputValidator.validate(
        evaluator_a_labels=("low", "high"),
        evaluator_b_labels=("low", "medium"),
    )
    CorrelationInputValidator.validate(
        x_values=(1.0, 2.0),
        y_values=(2.0, 3.0),
    )
    RegressionInputValidator.validate(
        actual_values=(1.0, 2.0),
        predicted_values=(1.1, 1.9),
    )
    BootstrapSamplingInputValidator.validate(
        values=(1.0, 2.0),
        bootstrap_iterations=10,
    )
    FleissKappaInputValidator.validate(
        label_matrix=(("yes", "yes"), ("no", "yes")),
    )


def test_category_and_alignment_input_validators_should_accept_aligned_series() -> None:
    CategoryMetricsInputValidator.validate(
        human_scores=(1.0, 2.0),
        llm_scores=(1.1, 1.9),
        human_labels=("low", "high"),
        llm_labels=("low", "high"),
        categories=("RAG", "Agents"),
    )
    EvaluatorAlignmentInputValidator.validate(
        human_scores=(1.0, 2.0),
        llm_scores=(1.1, 1.9),
        human_labels=("low", "high"),
        llm_labels=("low", "high"),
    )


@pytest.mark.parametrize(
    "validator_call",
    [
        lambda: AgreementInputValidator.validate(
            evaluator_a_labels=("low",), evaluator_b_labels=()
        ),
        lambda: CorrelationInputValidator.validate(x_values=(1.0,), y_values=(2.0,)),
        lambda: RegressionInputValidator.validate(
            actual_values=(), predicted_values=()
        ),
        lambda: BootstrapSamplingInputValidator.validate(
            values=(1.0,), bootstrap_iterations=0
        ),
        lambda: CategoryMetricsInputValidator.validate(
            human_scores=(1.0,),
            llm_scores=(1.0,),
            human_labels=("low",),
            llm_labels=("low",),
            categories=(),
        ),
        lambda: EvaluatorAlignmentInputValidator.validate(
            human_scores=(1.0,),
            llm_scores=(1.0, 2.0),
            human_labels=("low",),
            llm_labels=("low",),
        ),
        lambda: FleissKappaInputValidator.validate(label_matrix=(("yes",),)),
    ],
)
def test_input_validators_should_raise_for_invalid_inputs(validator_call) -> None:
    with pytest.raises(EvaluationValidationError):
        validator_call()


def test_snapshot_sequence_validators_should_validate_snapshot_instances() -> None:
    snapshot = _snapshot(experiment_id="experiment-1", score=0.80)

    BenchmarkAggregationInputValidator.validate(snapshots=(snapshot,))
    TrendVisualizationInputValidator.validate(snapshots=(snapshot,))

    with pytest.raises(EvaluationValidationError, match="snapshots cannot be empty"):
        BenchmarkAggregationInputValidator.validate(snapshots=())

    with pytest.raises(EvaluationValidationError, match=r"snapshots\[0\]"):
        TrendVisualizationInputValidator.validate(snapshots=(object(),))  # type: ignore[arg-type]
