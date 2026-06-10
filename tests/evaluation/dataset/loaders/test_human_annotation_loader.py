from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.evaluation.dataset.errors.evaluation_dataset_loading_error import (
    EvaluationDatasetLoadingError,
)
from src.evaluation.dataset.loaders.human_annotation_loader import (
    HumanAnnotationLoader,
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


def _valid_human_annotation_payload() -> list[dict[str, object]]:
    return [
        {
            "sample_id": "sample-1",
            "evaluator_id": "evaluator-1",
            "overall_score": 85.0,
            "technical_score": 90.0,
            "communication_score": 80.0,
            "feedback": "Strong human evaluation.",
        }
    ]


def test_human_annotation_loader_should_load_human_scores(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=_valid_human_annotation_payload(),
    )

    human_scores = HumanAnnotationLoader().load(
        file_path=file_path,
    )

    assert len(human_scores) == 1
    assert human_scores[0].sample_id == "sample-1"
    assert human_scores[0].evaluator_id == "evaluator-1"
    assert human_scores[0].overall_score == 85.0
    assert human_scores[0].technical_score == 90.0
    assert human_scores[0].communication_score == 80.0
    assert human_scores[0].feedback == "Strong human evaluation."


def test_human_annotation_loader_should_raise_for_missing_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "missing.json"

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="JSON file does not exist",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


def test_human_annotation_loader_should_raise_for_invalid_json(
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
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


def test_human_annotation_loader_should_raise_for_non_array_json(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload={
            "sample_id": "sample-1",
        },
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Human annotation file must contain a JSON array",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


def test_human_annotation_loader_should_raise_for_empty_array(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=[],
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Human annotation file cannot be empty",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


def test_human_annotation_loader_should_raise_for_non_object_record(
    tmp_path: Path,
) -> None:
    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=[
            "invalid-record",
        ],
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match=(
            "Human annotation record at index 0 "
            "must be a JSON object"
        ),
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


def test_human_annotation_loader_should_raise_for_missing_required_field(
    tmp_path: Path,
) -> None:
    payload = _valid_human_annotation_payload()
    del payload[0]["feedback"]

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="missing required fields",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


def test_human_annotation_loader_should_raise_for_invalid_string_field(
    tmp_path: Path,
) -> None:
    payload = _valid_human_annotation_payload()
    payload[0]["evaluator_id"] = 123

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="field 'evaluator_id' must be a string",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_annotation_loader_should_raise_for_invalid_numeric_field(
    tmp_path: Path,
    field_name: str,
) -> None:
    payload = _valid_human_annotation_payload()
    payload[0][field_name] = "invalid-score"

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match=f"field '{field_name}' must be numeric",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_annotation_loader_should_raise_for_boolean_numeric_field(
    tmp_path: Path,
    field_name: str,
) -> None:
    payload = _valid_human_annotation_payload()
    payload[0][field_name] = True

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match=f"field '{field_name}' must be numeric",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_annotation_loader_should_raise_for_score_below_zero(
    tmp_path: Path,
    field_name: str,
) -> None:
    payload = _valid_human_annotation_payload()
    payload[0][field_name] = -1.0

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Invalid HumanScore domain value",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "overall_score",
        "technical_score",
        "communication_score",
    ],
)
def test_human_annotation_loader_should_raise_for_score_above_hundred(
    tmp_path: Path,
    field_name: str,
) -> None:
    payload = _valid_human_annotation_payload()
    payload[0][field_name] = 101.0

    file_path = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=payload,
    )

    with pytest.raises(
        EvaluationDatasetLoadingError,
        match="Invalid HumanScore domain value",
    ):
        HumanAnnotationLoader().load(
            file_path=file_path,
        )