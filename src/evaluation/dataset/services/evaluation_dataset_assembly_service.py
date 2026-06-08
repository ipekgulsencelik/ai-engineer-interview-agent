from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.evaluation.dataset.entities.dataset_metadata import DatasetMetadata
from src.evaluation.dataset.entities.dataset_version import DatasetVersion
from src.evaluation.dataset.entities.evaluation_dataset import EvaluationDataset
from src.evaluation.dataset.enums.dataset_stage import DatasetStage
from src.evaluation.domain.entities import EvaluationSample, HumanScore, LLMScore


class EvaluationDatasetAssemblyService:
    """Application service for assembling evaluation datasets."""

    @staticmethod
    def assemble(
        *,
        dataset_id: str,
        dataset_name: str,
        dataset_version: str,
        description: str,
        samples: tuple[EvaluationSample, ...],
        human_scores: tuple[HumanScore, ...] = (),
        llm_scores: tuple[LLMScore, ...] = (),
        metadata: dict[str, Any] | None = None,
        created_by: str = "system",
        rubric_version: str = "1.0.0",
        evaluator_version: str = "1.0.0",
        source: str | None = None,
        stage: DatasetStage = DatasetStage.DEVELOPMENT,
        notes: str | None = None,
    ) -> EvaluationDataset:
        metadata_payload = dict(metadata or {})
        resolved_source = source or str(metadata_payload.get("source", "unknown"))
        metadata_payload.setdefault("source", resolved_source)
        metadata_payload["sample_count"] = len(samples)
        metadata_payload["human_score_count"] = len(human_scores)
        metadata_payload["llm_score_count"] = len(llm_scores)

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
                source=resolved_source,
                notes=notes,
                extras=metadata_payload,
            ),
            samples=samples,
            human_scores=human_scores,
            llm_scores=llm_scores,
        )
