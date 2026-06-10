from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.domain.enums.level import Level
from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.loaders.evaluation_sample_loader import (
    EvaluationSampleLoader,
)


def _write_json(
    *,
    tmp_path: Path,
    file_name: str,
    payload: object,
) -> Path:
    file_path = tmp_path / file_name

    file_path.write_text(
        json.dumps(
            payload,
        ),
        encoding="utf-8",
    )

    return file_path


def _valid_sample_payload() -> list[dict[str, object]]:
    return [
        {
            "sample_id": "sample-1",
            "question_id": "question-1",
            "question": "What is RAG?",
            "candidate_answer": (
                "RAG combines retrieval and generation."
            ),
            "expected_answer": (
                "Retrieval-Augmented Generation."
            ),
            "category": "RAG",
            "level": "jr",
            "retrieved_contexts": [
                "RAG improves grounding.",
            ],
            "metadata": {
                "source": "unit-test",
            },
        }
    ]


def test_evaluation_sample_loader_should_load_samples(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=_valid_sample_payload(),
    )

    samples = EvaluationSampleLoader().load(
        file_path=file_path,
    )

    assert len(samples) == 1
    assert samples[0].sample_id == "sample-1"
    assert samples[0].question_id == "question-1"
    assert samples[0].question == "What is RAG?"
    assert samples[0].candidate_answer == (
        "RAG combines retrieval and generation."
    )
    assert samples[0].expected_answer == (
        "Retrieval-Augmented Generation."
    )
    assert samples[0].category == "RAG"
    assert samples[0].level is Level.JR
    assert samples[0].retrieved_contexts == (
        "RAG improves grounding.",
    )
    assert samples[0].metadata == {
        "source": "unit-test",
    }


def test_evaluation_sample_loader_should_raise_for_missing_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "missing.json"

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="JSON file does not exist",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_invalid_json(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "invalid.json"
    file_path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Invalid JSON file",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_non_array_json(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload={
            "sample_id": "sample-1",
        },
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Evaluation sample file must contain a JSON array",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_empty_array(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=[],
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Evaluation sample file cannot be empty",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_non_object_record(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=[
            "invalid-record",
        ],
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match=(
            "Evaluation sample record at index 0 "
            "must be a JSON object"
        ),
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_missing_required_field(
    tmp_path: Path,
) -> None:
    payload = _valid_sample_payload()
    del payload[0]["question"]

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="missing required fields",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_invalid_level(
    tmp_path: Path,
) -> None:
    payload = _valid_sample_payload()
    payload[0]["level"] = "invalid-level"

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="has invalid level",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_invalid_contexts_type(
    tmp_path: Path,
) -> None:
    payload = _valid_sample_payload()
    payload[0]["retrieved_contexts"] = "invalid-contexts"

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="field 'retrieved_contexts' must be a list",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_invalid_context_item(
    tmp_path: Path,
) -> None:
    payload = _valid_sample_payload()
    payload[0]["retrieved_contexts"] = [
        123,
    ]

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match=r"retrieved_contexts\[0\] must be a string",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )


def test_evaluation_sample_loader_should_raise_for_invalid_metadata_type(
    tmp_path: Path,
) -> None:
    payload = _valid_sample_payload()
    payload[0]["metadata"] = []

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="samples.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="field 'metadata' must be an object",
    ):
        EvaluationSampleLoader().load(
            file_path=file_path,
        )