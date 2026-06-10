from __future__ import annotations

import pytest

from src.domain.enums.level import Level
from src.evaluation.domain.entities.evaluation_sample import (
    EvaluationSample,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def test_evaluation_sample_should_create_successfully() -> None:
    sample = EvaluationSample(
        sample_id="sample-1",
        question_id="question-1",
        question="What is RAG?",
        candidate_answer=(
            "RAG combines retrieval and generation."
        ),
        expected_answer=(
            "Retrieval-Augmented Generation."
        ),
        category="RAG",
        level=Level.JR,
        retrieved_contexts=(
            "RAG improves grounding.",
        ),
        metadata={},
    )

    assert sample.sample_id == "sample-1"
    assert sample.question_id == "question-1"
    assert sample.question == "What is RAG?"
    assert sample.candidate_answer == (
        "RAG combines retrieval and generation."
    )
    assert sample.expected_answer == (
        "Retrieval-Augmented Generation."
    )
    assert sample.category == "RAG"
    assert sample.level is Level.JR
    assert sample.retrieved_contexts == (
        "RAG improves grounding.",
    )
    assert sample.metadata == {}


def test_evaluation_sample_should_raise_for_empty_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_id cannot be empty",
    ):
        EvaluationSample(
            sample_id="",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_empty_question_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="question_id cannot be empty",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_empty_question() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="question cannot be empty",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_empty_candidate_answer() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="candidate_answer cannot be empty",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_empty_expected_answer() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="expected_answer cannot be empty",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_empty_category() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="category cannot be empty",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="",
            level=Level.JR,
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_invalid_level() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="level must be a Level enum",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level="JR",  # type: ignore[arg-type]
            retrieved_contexts=(),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_invalid_retrieved_context_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="retrieved_contexts must be tuple",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=["context"],  # type: ignore[arg-type]
            metadata={},
        )


def test_evaluation_sample_should_raise_for_invalid_retrieved_context_item() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"retrieved_contexts\[0\] must be str",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(1,),  # type: ignore[arg-type]
            metadata={},
        )


def test_evaluation_sample_should_raise_for_empty_retrieved_context_item() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"retrieved_contexts\[0\] cannot be empty",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=("   ",),
            metadata={},
        )


def test_evaluation_sample_should_raise_for_invalid_metadata_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="metadata must be dict",
    ):
        EvaluationSample(
            sample_id="sample-1",
            question_id="question-1",
            question="What is RAG?",
            candidate_answer="answer",
            expected_answer="expected",
            category="RAG",
            level=Level.JR,
            retrieved_contexts=(),
            metadata=[],  # type: ignore[arg-type]
        )


def test_evaluation_sample_should_be_immutable() -> None:
    sample = EvaluationSample(
        sample_id="sample-1",
        question_id="question-1",
        question="What is RAG?",
        candidate_answer="answer",
        expected_answer="expected",
        category="RAG",
        level=Level.JR,
        retrieved_contexts=(),
        metadata={},
    )

    with pytest.raises(
        AttributeError,
    ):
        sample.sample_id = "changed"  # type: ignore[misc]