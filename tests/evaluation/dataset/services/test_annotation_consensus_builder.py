from __future__ import annotations

import pytest

from src.evaluation.domain.builders.sample_annotation_consensus_builder import (
    SampleAnnotationConsensusBuilder,
)
from src.evaluation.domain.entities import (
    HumanScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _human_score(
    *,
    sample_id: str = "sample-1",
    evaluator_id: str = "evaluator-1",
    overall_score: float = 80.0,
) -> HumanScore:
    return HumanScore(
        sample_id=sample_id,
        evaluator_id=evaluator_id,
        overall_score=overall_score,
        technical_score=overall_score,
        communication_score=overall_score,
        feedback="Valid feedback.",
    )


def test_sample_annotation_consensus_builder_should_build_consensus() -> None:
    consensus = SampleAnnotationConsensusBuilder.build(
        scores=(
            _human_score(
                evaluator_id="evaluator-1",
                overall_score=80.0,
            ),
            _human_score(
                evaluator_id="evaluator-2",
                overall_score=90.0,
            ),
        ),
    )

    assert consensus.sample_id == "sample-1"
    assert consensus.annotator_count == 2
    assert consensus.consensus_score == 85.0
    assert consensus.min_score == 80.0
    assert consensus.max_score == 90.0
    assert consensus.score_range == 10.0


def test_sample_annotation_consensus_builder_should_build_for_single_score() -> None:
    consensus = SampleAnnotationConsensusBuilder.build(
        scores=(
            _human_score(
                evaluator_id="evaluator-1",
                overall_score=88.0,
            ),
        ),
    )

    assert consensus.sample_id == "sample-1"
    assert consensus.annotator_count == 1
    assert consensus.consensus_score == 88.0
    assert consensus.min_score == 88.0
    assert consensus.max_score == 88.0
    assert consensus.score_range == 0.0


def test_sample_annotation_consensus_builder_should_raise_for_empty_scores() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="scores cannot be empty",
    ):
        SampleAnnotationConsensusBuilder.build(
            scores=(),
        )


def test_sample_annotation_consensus_builder_should_raise_for_multiple_sample_ids() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="all scores must belong to the same sample",
    ):
        SampleAnnotationConsensusBuilder.build(
            scores=(
                _human_score(
                    sample_id="sample-1",
                    evaluator_id="evaluator-1",
                    overall_score=80.0,
                ),
                _human_score(
                    sample_id="sample-2",
                    evaluator_id="evaluator-2",
                    overall_score=90.0,
                ),
            ),
        )


def test_sample_annotation_consensus_builder_should_use_overall_score_only() -> None:
    consensus = SampleAnnotationConsensusBuilder.build(
        scores=(
            HumanScore(
                sample_id="sample-1",
                evaluator_id="evaluator-1",
                overall_score=70.0,
                technical_score=100.0,
                communication_score=100.0,
                feedback="Valid feedback.",
            ),
            HumanScore(
                sample_id="sample-1",
                evaluator_id="evaluator-2",
                overall_score=90.0,
                technical_score=0.0,
                communication_score=0.0,
                feedback="Valid feedback.",
            ),
        ),
    )

    assert consensus.consensus_score == 80.0
    assert consensus.min_score == 70.0
    assert consensus.max_score == 90.0
    assert consensus.score_range == 20.0