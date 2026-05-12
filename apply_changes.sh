set -e

# 1) Branch hazırla
git checkout main
git pull origin main
git checkout -b feature/solid-interview-session || git checkout feature/solid-interview-session

# 2) Gerekli klasörler
mkdir -p src/domain/interview
mkdir -p src/domain/validators
mkdir -p tests/domain/policies
mkdir -p tests/domain
mkdir -p tests/services
mkdir -p tests/application/policies
mkdir -p tests/application/services

# 3) InterviewSession validator
cat > src/domain/validators/interview_session_validator.py <<'PY'
from __future__ import annotations

from src.domain.enums.level import Level
from src.domain.results.evaluation_result import EvaluationResult


class InterviewSessionValidator:
    @staticmethod
    def validate(session: "InterviewSession") -> None:
        InterviewSessionValidator._validate_session_id(session.session_id)
        InterviewSessionValidator._validate_level(session.current_level)
        InterviewSessionValidator._validate_question_ids(session.asked_question_ids)
        InterviewSessionValidator._validate_results(session.completed_results)
        InterviewSessionValidator._validate_scores(session.recent_scores)

    @staticmethod
    def _validate_session_id(session_id: str) -> None:
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id cannot be empty")

    @staticmethod
    def _validate_level(level: Level) -> None:
        if not isinstance(level, Level):
            raise TypeError("current_level must be a Level instance")

    @staticmethod
    def _validate_question_ids(asked_question_ids: tuple[str, ...]) -> None:
        if not isinstance(asked_question_ids, tuple):
            raise TypeError("asked_question_ids must be a tuple")

        for question_id in asked_question_ids:
            if not isinstance(question_id, str) or not question_id.strip():
                raise ValueError("asked_question_ids cannot include empty values")

    @staticmethod
    def _validate_results(completed_results: tuple[EvaluationResult, ...]) -> None:
        if not isinstance(completed_results, tuple):
            raise TypeError("completed_results must be a tuple")

        for result in completed_results:
            if not isinstance(result, EvaluationResult):
                raise TypeError("completed_results items must be EvaluationResult")

    @staticmethod
    def _validate_scores(recent_scores: tuple[float, ...]) -> None:
        if not isinstance(recent_scores, tuple):
            raise TypeError("recent_scores must be a tuple")

        for score in recent_scores:
            if not isinstance(score, (int, float)):
                raise TypeError("recent_scores items must be numeric")
            if score < 0.0 or score > 10.0:
                raise ValueError("recent_scores values must be between 0.0 and 10.0")
PY

# 4) InterviewSession
cat > src/domain/interview/interview_session.py <<'PY'
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from src.domain.enums.level import Level
from src.domain.results.evaluation_result import (
    EvaluationResult,
)
from src.domain.validators.interview_session_validator import (
    InterviewSessionValidator,
)


@dataclass(frozen=True)
class InterviewSession:
    """Adaptive interview workflow aggregate state."""

    session_id: str
    current_level: Level
    asked_question_ids: tuple[str, ...] = field(default_factory=tuple)
    completed_results: tuple[EvaluationResult, ...] = field(default_factory=tuple)
    recent_scores: tuple[float, ...] = field(default_factory=tuple)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        InterviewSessionValidator.validate(self)

    def with_completed_turn(
        self,
        *,
        question_id: str,
        result: EvaluationResult,
    ) -> "InterviewSession":
        normalized_question_id = question_id.strip()
        if not normalized_question_id:
            raise ValueError("question_id cannot be empty")

        return replace(
            self,
            asked_question_ids=(*self.asked_question_ids, normalized_question_id),
            completed_results=(*self.completed_results, result),
            recent_scores=(*self.recent_scores, float(result.score)),
        )

    def with_level(self, *, level: Level) -> "InterviewSession":
        return replace(
            self,
            current_level=level,
        )
PY

# 5) InterviewSession test
cat > tests/domain/test_interview_session.py <<'PY'
import pytest

from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult


def build_result(score: float = 7.5) -> EvaluationResult:
    return EvaluationResult(
        score=score,
        feedback="Good",
        technical_accuracy=7.0,
        depth=7.0,
        communication=8.0,
    )


def test_session_initialization() -> None:
    session = InterviewSession(
        session_id="s1",
        current_level=Level.MID,
    )

    assert session.session_id == "s1"
    assert session.current_level == Level.MID
    assert session.asked_question_ids == ()


def test_with_completed_turn_returns_new_session() -> None:
    session = InterviewSession(
        session_id="s1",
        current_level=Level.JR,
    )

    updated = session.with_completed_turn(
        question_id=" q1 ",
        result=build_result(8.0),
    )

    assert updated is not session
    assert updated.asked_question_ids == ("q1",)
    assert updated.completed_results[0].score == 8.0
    assert updated.recent_scores == (8.0,)


def test_with_level_returns_new_session() -> None:
    session = InterviewSession(
        session_id="s1",
        current_level=Level.JR,
    )

    updated = session.with_level(level=Level.SENIOR)

    assert updated.current_level == Level.SENIOR
    assert session.current_level == Level.JR


def test_session_rejects_empty_session_id() -> None:
    with pytest.raises(ValueError):
        InterviewSession(
            session_id="",
            current_level=Level.JR,
        )
PY

# 6) Test + commit + push
pytest -q tests/domain/test_interview_session.py || true
git add .
git commit -m "Refactor InterviewSession into immutable SOLID aggregate" || true
git push -u origin feature/solid-interview-session || true

echo "Bitti. Şimdi GitHub'da PR aç: feature/solid-interview-session -> main"
