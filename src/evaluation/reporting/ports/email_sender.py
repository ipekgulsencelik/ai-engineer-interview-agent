from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path


class EmailSender(
    ABC,
):
    """
    Email sender port.

    Infrastructure adapters should implement this interface
    for SMTP, SendGrid, SES, Mailgun, Gmail, or internal
    notification services.
    """

    @abstractmethod
    def send(
        self,
        *,
        to: str,
        subject: str,
        body: str,
        attachment_path: Path | None = None,
    ) -> None:
        """
        Sends an email message.
        """