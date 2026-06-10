from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.dataset.entities.dataset_metadata import (
    DatasetMetadata,
)
from src.evaluation.dataset.entities.dataset_version import (
    DatasetVersion,
)
from src.evaluation.dataset.validators.evaluation_dataset_validator import (
    EvaluationDatasetValidator,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EvaluationDataset:
    """
    Immutable evaluation dataset aggregate.
    """

    dataset_id: str
    dataset_name: str
    dataset_version: DatasetVersion
    description: str
    metadata: DatasetMetadata
    samples: tuple[EvaluationSample, ...]
    human_scores: tuple[HumanScore, ...] = ()
    llm_scores: tuple[LLMScore, ...] = ()

    def __post_init__(self) -> None:
        EvaluationDatasetValidator.validate(
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            dataset_version=self.dataset_version,
            description=self.description,
            metadata=self.metadata,
            samples=self.samples,
            human_scores=self.human_scores,
            llm_scores=self.llm_scores,
        )

    @property
    def sample_ids(self) -> tuple[str, ...]:
        return tuple(
            sample.sample_id
            for sample in self.samples
        )

    @property
    def sample_count(self) -> int:
        return len(self.samples)

    @property
    def human_score_count(self) -> int:
        return len(self.human_scores)

    @property
    def llm_score_count(self) -> int:
        return len(self.llm_scores)