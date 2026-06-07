from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.dataset.entities.dataset_metadata import (
    DatasetMetadata,
)
from src.evaluation.dataset.entities.dataset_version import (
    DatasetVersion,
)
from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)
from src.evaluation.dataset.enums.dataset_stage import (
    DatasetStage,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
)


class EvaluationDatasetAssemblyService:
    """
    Application service for assembling evaluation datasets.
    """

    @staticmethod
    def assemble(
        *,
        dataset_id: str,
        dataset_name: str,
        dataset_version: str,
        description: str,
        samples: tuple[EvaluationSample, ...],
        created_by: str,
        rubric_version: str,
        evaluator_version: str,
        source: str,
        stage: DatasetStage = DatasetStage.DEVELOPMENT,
        human_scores: tuple[HumanScore, ...] = (),
        llm_scores: tuple[LLMScore, ...] = (),
        notes: str | None = None,
    ) -> EvaluationDataset:
        return EvaluationDataset(
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            dataset_version=DatasetVersion(
                version=dataset_version,
                stage=stage,
                created_by=created_by,
                description=description,
            ),
            description=description,
            metadata=DatasetMetadata(
                created_at=datetime.now(timezone.utc),
                rubric_version=rubric_version,
                evaluator_version=evaluator_version,
                source=source,
                notes=notes,
            ),
            samples=samples,
            human_scores=human_scores,
            llm_scores=llm_scores,
        )