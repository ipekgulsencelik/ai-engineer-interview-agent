from __future__ import annotations


class LogValueNormalizer:
    """
    Logging-safe value normalization helper.
    """

    @staticmethod
    def normalize(
        value: object,
    ) -> object:
        return getattr(
            value,
            "value",
            value,
        )