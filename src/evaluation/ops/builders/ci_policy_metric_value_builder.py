from __future__ import annotations


class CIPolicyMetricValueBuilder:
    """
    Builds numeric dashboard value for CI policy status.
    """

    @staticmethod
    def build(
        *,
        deployment_allowed: bool,
    ) -> float:
        if deployment_allowed:
            return 1.0

        return 0.0