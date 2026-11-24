from __future__ import annotations

from typing import Annotated, TypeAlias

from fastapi import Depends, Request

from src.api.app_state import get_service_container
from src.api.storage.interview_session_store import InMemoryInterviewSessionStore
from src.application.services.interview_session_service import (
    InterviewSessionService,
)
from src.infrastructure.containers.service_container import ServiceContainer

ServiceContainerDependency: TypeAlias = Annotated[
    ServiceContainer,
    Depends(get_service_container),
]


def get_interview_session_service(
    container: ServiceContainerDependency,
) -> InterviewSessionService:
    return container.interview_session_service


def get_interview_session_store(request: Request) -> InMemoryInterviewSessionStore:
    store = getattr(request.app.state, "interview_sessions", None)
    if not isinstance(store, InMemoryInterviewSessionStore):
        raise RuntimeError("Interview session store is not initialized.")
    return store


InterviewSessionServiceDependency: TypeAlias = Annotated[
    InterviewSessionService,
    Depends(get_interview_session_service),
]

InterviewSessionStoreDependency: TypeAlias = Annotated[
    InMemoryInterviewSessionStore,
    Depends(get_interview_session_store),
]
