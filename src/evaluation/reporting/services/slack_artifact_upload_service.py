from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.slack_client import (
    SlackClient,
)


class SlackArtifactUploadService:
    """
    Handles optional Slack artifact upload.
    """

    def __init__(
        self,
        *,
        slack_client: SlackClient,
    ) -> None:
        self._slack_client = slack_client

    def upload_if_requested(
        self,
        *,
        report: ReportArtifact,
        channel: str,
        upload_artifact: bool,
    ) -> None:
        if not upload_artifact:
            return

        if not report.path:
            return

        path = Path(
            report.path,
        )

        if not path.exists():
            return

        if not path.is_file():
            return

        self._slack_client.upload_file(
            channel=channel,
            file_path=str(
                path,
            ),
            title=report.title,
        )