from __future__ import annotations

from datetime import UTC
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.enums.experiment_artifact_type import (
    ExperimentArtifactType,
)
from src.evaluation.reporting.resolvers.content_type_resolver import (
    ContentTypeResolver,
)


class ReportArtifactFactory:
    """
    Factory for creating ReportArtifact entities.
    """

    def __init__(
        self,
        *,
        content_type_resolver: ContentTypeResolver,
    ) -> None:
        self._content_type_resolver = content_type_resolver

    def create(
        self,
        *,
        title: str,
        report_type: str,
        run_id: str,
        experiment_id: str,
        report_format: str,
        output_path: Path,
        content: str | None,
        generated_by: str | None = None,
        description: str | None = None,
    ) -> ReportArtifact:
        return ReportArtifact(
            report_id=str(
                uuid4(),
            ),
            artifact_id=str(
                uuid4(),
            ),
            run_id=run_id,
            experiment_id=experiment_id,
            title=title,
            report_type=report_type,
            artifact_type=ExperimentArtifactType.REPORT,
            path=str(
                output_path,
            ),
            content=content,
            uri=None,
            storage_backend=None,
            format=report_format,
            content_type=self._content_type_resolver.resolve(
                report_format=report_format,
            ),
            size_bytes=(
                output_path.stat().st_size
                if output_path.exists()
                else None
            ),
            checksum=None,
            generated_by=generated_by,
            created_at=datetime.now(
                UTC,
            ),
            description=description,
            tags=(
                report_type,
                report_format,
            ),
            metadata=None,
        )