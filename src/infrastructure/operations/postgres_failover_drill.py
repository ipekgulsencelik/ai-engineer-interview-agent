"""Fail-closed failover drill against an isolated CloudNativePG test cluster.

The production operator owns automatic election; this tool only simulates a
primary pod loss in a *dedicated* drill namespace. No production failover
trigger is exposed by this script.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

_DRILL_NAMESPACE = "interview-db-drill"
_DRILL_CLUSTER = "interview-db-drill"
_APPROVAL = "I_AUTHORIZE_DESTRUCTIVE_DRILL_IN_ISOLATED_CLUSTER"


@dataclass(frozen=True, slots=True)
class ClusterStatus:
    primary: str
    instances: int
    ready_instances: int


class FailoverDrillPort(Protocol):
    def status(self) -> ClusterStatus: ...
    def delete_primary(self, pod: str) -> None: ...
    def new_primary_is_writable(self, pod: str) -> bool: ...


class KubectlFailoverAdapter:
    """Infrastructure shell adapter; fixed argv, no shell interpolation."""

    def __init__(self, *, namespace: str, cluster: str) -> None:
        self._namespace = namespace
        self._cluster = cluster

    def _kubectl(self, *args: str) -> str:
        result = subprocess.run(
            ["kubectl", "-n", self._namespace, *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip()

    def status(self) -> ClusterStatus:
        output = self._kubectl(
            "get", "cluster", self._cluster, "-o", "json"
        )
        parsed = json.loads(output)
        raw = parsed.get("status", {})
        spec = parsed.get("spec", {})
        return ClusterStatus(
            primary=str(raw.get("currentPrimary") or ""),
            instances=int(spec.get("instances") or 0),
            ready_instances=int(raw.get("readyInstances") or 0),
        )

    def delete_primary(self, pod: str) -> None:
        self._kubectl(
            "delete", "pod", pod, "--wait=false",
            "--grace-period=0",
        )

    def new_primary_is_writable(self, pod: str) -> bool:
        result = self._kubectl(
            "exec", pod, "-c", "postgres", "--",
            "psql", "-U", "postgres", "-d", "postgres",
            "-tAX", "-c", "SELECT NOT pg_is_in_recovery()",
        )
        return result == "t"


class ControlledFailoverVerifier:
    """Application orchestration over the narrow cluster operations port."""

    def __init__(
        self,
        *,
        adapter: FailoverDrillPort,
        deadline_seconds: int = 180,
        sleep: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        if type(deadline_seconds) is not int or not 30 <= deadline_seconds <= 900:
            raise ValueError("deadline_seconds must be in [30, 900]")
        self._adapter = adapter
        self._deadline_seconds = deadline_seconds
        self._sleep = sleep
        self._monotonic = monotonic

    def execute(
        self, *, namespace: str, cluster: str, approval: str
    ) -> tuple[str, str]:
        if (
            namespace != _DRILL_NAMESPACE
            or cluster != _DRILL_CLUSTER
            or approval != _APPROVAL
        ):
            raise PermissionError(
                "destructive drill restricted to explicitly approved test cluster"
            )
        before = self._adapter.status()
        if (
            not before.primary
            or before.instances != 3
            or before.ready_instances != 3
        ):
            raise RuntimeError(
                "drill requires three healthy replicas and a known primary"
            )

        self._adapter.delete_primary(before.primary)
        deadline = self._monotonic() + self._deadline_seconds
        while self._monotonic() < deadline:
            now = self._adapter.status()
            if (
                now.primary
                and now.primary != before.primary
                and now.ready_instances >= 2
                and self._adapter.new_primary_is_writable(now.primary)
            ):
                return before.primary, now.primary
            self._sleep(3)
        raise TimeoutError(
            "operator failover did not complete within drill deadline"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Destructive CloudNativePG failover TEST only"
    )
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--cluster", required=True)
    parser.add_argument("--approval", required=True)
    parser.add_argument("--deadline-seconds", type=int, default=180)
    args = parser.parse_args()
    verifier = ControlledFailoverVerifier(
        adapter=KubectlFailoverAdapter(
            namespace=args.namespace, cluster=args.cluster,
        ),
        deadline_seconds=args.deadline_seconds,
    )
    old, new = verifier.execute(
        namespace=args.namespace,
        cluster=args.cluster,
        approval=args.approval,
    )
    print(f"FAILOVER VERIFIED: old={old}, new={new}")


if __name__ == "__main__":
    main()
