from __future__ import annotations

import pytest

from src.evaluation.dataset.entities.dataset_version import (
    DatasetVersion,
)
from src.evaluation.dataset.enums.dataset_stage import (
    DatasetStage,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def test_dataset_version_should_create_successfully() -> None:
    dataset_version = DatasetVersion(
        version="1.0.0",
        stage=DatasetStage.DEVELOPMENT,
        created_by="system",
        description="Initial dataset version.",
    )

    assert dataset_version.version == "1.0.0"
    assert dataset_version.stage is DatasetStage.DEVELOPMENT
    assert dataset_version.created_by == "system"
    assert dataset_version.description == "Initial dataset version."


def test_dataset_version_should_raise_for_empty_version() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="version cannot be empty",
    ):
        DatasetVersion(
            version="",
            stage=DatasetStage.DEVELOPMENT,
            created_by="system",
            description="Initial dataset version.",
        )


def test_dataset_version_should_raise_for_invalid_stage() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="stage must be a DatasetStage enum",
    ):
        DatasetVersion(
            version="1.0.0",
            stage="DEVELOPMENT",  # type: ignore[arg-type]
            created_by="system",
            description="Initial dataset version.",
        )


def test_dataset_version_should_raise_for_empty_created_by() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="created_by cannot be empty",
    ):
        DatasetVersion(
            version="1.0.0",
            stage=DatasetStage.DEVELOPMENT,
            created_by="",
            description="Initial dataset version.",
        )


def test_dataset_version_should_raise_for_empty_description() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="description cannot be empty",
    ):
        DatasetVersion(
            version="1.0.0",
            stage=DatasetStage.DEVELOPMENT,
            created_by="system",
            description="",
        )


def test_dataset_version_should_be_immutable() -> None:
    dataset_version = DatasetVersion(
        version="1.0.0",
        stage=DatasetStage.DEVELOPMENT,
        created_by="system",
        description="Initial dataset version.",
    )

    with pytest.raises(
        AttributeError,
    ):
        dataset_version.version = "2.0.0"  # type: ignore[misc]