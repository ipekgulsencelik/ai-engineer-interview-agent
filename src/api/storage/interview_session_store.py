from __future__ import annotations

import secrets
import threading
from collections import OrderedDict

from src.application.services.interview_session_service import InterviewSession

DEFAULT_MAX_SESSIONS = 1000


class InterviewSessionNotFoundError(KeyError):
    pass


class InMemoryInterviewSessionStore:
    """
    Process-local interview session store.

    Sessions are lost on restart and not shared between workers; durable,
    per-user persistence is Faz 4 (longitudinal tracking). The oldest
    sessions are evicted beyond max_sessions to bound memory.
    """

    def __init__(self, *, max_sessions: int = DEFAULT_MAX_SESSIONS) -> None:
        self._sessions: OrderedDict[str, InterviewSession] = OrderedDict()
        self._max_sessions = max_sessions
        self._lock = threading.Lock()

    def create(self, session: InterviewSession) -> str:
        session_id = secrets.token_urlsafe(16)
        with self._lock:
            self._sessions[session_id] = session
            while len(self._sessions) > self._max_sessions:
                self._sessions.popitem(last=False)
        return session_id

    def get(self, session_id: str) -> InterviewSession:
        with self._lock:
            try:
                return self._sessions[session_id]
            except KeyError:
                raise InterviewSessionNotFoundError(session_id) from None

    def save(self, session_id: str, session: InterviewSession) -> None:
        with self._lock:
            if session_id not in self._sessions:
                raise InterviewSessionNotFoundError(session_id)
            self._sessions[session_id] = session
            self._sessions.move_to_end(session_id)
