"""Destructive failover controls and deterministic primary promotion tests."""

from __future__ import annotations

import json
import subprocess

import pytest

from src.infrastructure.operations.postgres_failover_drill import (
    ClusterStatus,
    ControlledFailoverVerifier,
    KubectlFailoverAdapter,
)

GOOD = ClusterStatus("interview-db-drill-1", 3, 3)
NEW = ClusterStatus("interview-db-drill-2", 3, 2)
APPROVAL = "I_AUTHORIZE_DESTRUCTIVE_DRILL_IN_ISOLATED_CLUSTER"


class StubCluster:
    def __init__(
        self,
        statuses: tuple[ClusterStatus, ...] = (GOOD, NEW),
        writable: bool = True,
    ) -> None:
        self.statuses = list(statuses)
        self.writable = writable
        self.deleted: list[str] = []
        self.queried: list[str] = []

    def status(self) -> ClusterStatus:
        if len(self.statuses) > 1:
            return self.statuses.pop(0)
        return self.statuses[0]

    def delete_primary(self, pod: str) -> None:
        self.deleted.append(pod)

    def new_primary_is_writable(self, pod: str) -> bool:
        self.queried.append(pod)
        return self.writable


def _run(
    client: StubCluster, *,
    ns: str = "interview-db-drill",
    cluster: str = "interview-db-drill",
    approval: str = APPROVAL,
) -> tuple[str, str]:
    time_value = [0.0]

    def clock() -> float:
        return time_value[0]

    def tick(seconds: float) -> None:
        time_value[0] += seconds

    return ControlledFailoverVerifier(
        adapter=client,
        monotonic=clock,
        sleep=tick,
        deadline_seconds=30,
    ).execute(namespace=ns, cluster=cluster, approval=approval)


def test_failover_detects_new_writable_primary() -> None:
    client = StubCluster()
    assert _run(client) == ("interview-db-drill-1", "interview-db-drill-2")
    assert client.deleted == ["interview-db-drill-1"]
    assert client.queried == ["interview-db-drill-2"]


@pytest.mark.parametrize(
    ("ns", "cluster", "approval"),
    [
        ("interview-db", "interview-db-primary", APPROVAL),
        ("default", "interview-db-drill", APPROVAL),
        ("interview-db-drill", "interview-db-primary", APPROVAL),
        ("interview-db-drill", "interview-db-drill", "no"),
    ],
)
def test_production_or_missing_approval_never_deletes_pod(
    ns: str, cluster: str, approval: str
) -> None:
    client = StubCluster()
    with pytest.raises(PermissionError, match="restricted"):
        _run(client, ns=ns, cluster=cluster, approval=approval)
    assert client.deleted == []


@pytest.mark.parametrize(
    "bad",
    [
        ClusterStatus("", 3, 3),
        ClusterStatus("pod-a", 2, 2),
        ClusterStatus("pod-a", 3, 2),
    ],
)
def test_unhealthy_cluster_never_runs_destructive_drill(
    bad: ClusterStatus,
) -> None:
    client = StubCluster((bad, NEW))
    with pytest.raises(RuntimeError, match="three healthy"):
        _run(client)
    assert client.deleted == []


def test_failover_timeout_is_reported_not_falsely_successful() -> None:
    client = StubCluster((GOOD, GOOD))
    with pytest.raises(TimeoutError, match="did not complete"):
        _run(client)
    assert client.deleted == ["interview-db-drill-1"]


def test_new_primary_must_accept_writable_sql() -> None:
    client = StubCluster(writable=False)
    with pytest.raises(TimeoutError, match="did not complete"):
        _run(client)
    assert client.queried
    assert client.deleted == ["interview-db-drill-1"]


@pytest.mark.parametrize("seconds", [0, 29, 901, True])
def test_timeout_bounds(seconds: int) -> None:
    with pytest.raises(ValueError, match="deadline_seconds"):
        ControlledFailoverVerifier(
            adapter=StubCluster(), deadline_seconds=seconds
        )


def test_kubectl_uses_argv_not_shell(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        if "get" in argv:
            output = json.dumps({
                "spec": {"instances": 3},
                "status": {
                    "currentPrimary": "interview-db-drill-1",
                    "readyInstances": 3,
                },
            })
        else:
            output = "t"
        return subprocess.CompletedProcess(argv, 0, stdout=output, stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    adapter = KubectlFailoverAdapter(
        namespace="interview-db-drill", cluster="interview-db-drill"
    )
    assert adapter.status() == GOOD
    assert adapter.new_primary_is_writable("interview-db-drill-2")
    adapter.delete_primary("interview-db-drill-1")
    assert calls[0][:4] == [
        "kubectl", "-n", "interview-db-drill", "get"
    ]
    assert all("bash" not in call and "sh" not in call for call in calls)
    assert calls[-1][-2:] == ["--wait=false", "--grace-period=0"]
