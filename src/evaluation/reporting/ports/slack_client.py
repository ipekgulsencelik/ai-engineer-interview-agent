from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class SlackClient(
    ABC,
):
    """
    Slack delivery port.

    Infrastructure adapters should implement this
    interface using Slack SDK, incoming webhooks,
    or internal messaging gateways.
    """

    @abstractmethod
    def post_message(
        self,
        *,
        channel: str,
        message: str,
    ) -> None:
        """
        Sends a Slack message.
        """

    @abstractmethod
    def upload_file(
        self,
        *,
        channel: str,
        file_path: str,
        title: str,
    ) -> None:
        """
        Uploads a file to Slack.
        """