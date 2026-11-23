"""Run an adaptive interview in the terminal.

Examples:
    uv run python -m src.scripts.run_interview
    uv run python -m src.scripts.run_interview --level MID --skills python,langchain
    uv run python -m src.scripts.run_interview --demo          # scripted answers
    uv run python -m src.scripts.run_interview --semantic      # use the Chroma index

Answers are scored by the offline keyword-coverage evaluator. It is a
transparent heuristic for local runs; the Groq rubric evaluator is used by the
production path once configured.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from src.application.services.interview_session_service import (
    AnswerOutcome,
    InterviewSession,
    InterviewSessionService,
)
from src.domain.entities.question import Question
from src.infrastructure.evaluators.keyword_coverage_evaluator import (
    KeywordCoverageEvaluator,
)
from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)
from src.services.weighted_scoring_engine import WeightedScoringEngine

DEFAULT_BANK = Path("data/question_bank/questions.json")


def build_service(*, bank: Path, semantic: bool) -> InterviewSessionService:
    retriever = None
    if semantic:
        from src.infrastructure.containers.retrieval_container import (
            RetrievalContainer,
        )

        retrieval = RetrievalContainer().question_retrieval_service

        def retriever(*, query, context, top_k):  # type: ignore[no-redef]
            return [r.question for r in retrieval.retrieve(query=query, context=context, top_k=top_k)]

    return InterviewSessionService(
        question_repository=JsonQuestionRepositoryBuilder.build_default(file_path=bank),
        scoring_engine=WeightedScoringEngine(),
        evaluator=KeywordCoverageEvaluator(),
        retriever=retriever,
    )


def demo_answer(question: Question, index: int) -> str:
    """Scripted answers: strong for a while, then weak, to show level changes."""
    if index % 6 < 3:
        points = ". ".join(question.expected_points)
        return f"{question.ideal_answer_hint} In more detail: {points}. Keywords: {', '.join(question.keywords)}."
    return "I am not sure, I have not worked with this."


def run(
    service: InterviewSessionService,
    session: InterviewSession,
    answer_for: Callable[[Question, int], str | None],
    out=print,
) -> InterviewSession:
    index = 0
    while not session.is_finished:
        session, question = service.next_question(session)
        out("")
        out(f"[{index + 1}/{session.max_questions}] {question.level} · {question.category} · {question.question_type}")
        out(f"Q: {question.text}")
        answer = answer_for(question, index)
        if answer is None:  # user quit
            break
        outcome: AnswerOutcome = service.submit_answer(session, answer=answer)
        session = outcome.session
        ev = outcome.turn.evaluation
        out(f"   score {ev.score:.1f}/10  (technical {ev.technical_accuracy:.1f} · depth {ev.depth:.1f} · communication {ev.communication:.1f})")
        out(f"   {ev.feedback}")
        if outcome.level_changed:
            out(f"   >>> level {outcome.turn.level_before} -> {outcome.turn.level_after}")
        index += 1
    return session


def summary(session: InterviewSession) -> str:
    if not session.turns:
        return "No answers recorded."
    by_category: dict[str, list[float]] = {}
    for turn in session.turns:
        by_category.setdefault(str(turn.question.category), []).append(turn.evaluation.score)
    lines = [
        "",
        "=" * 60,
        f"Final level: {session.current_level}   Answers: {len(session.turns)}   "
        f"Average: {sum(session.scores) / len(session.scores):.1f}/10",
        "-" * 60,
    ]
    for category, scores in sorted(by_category.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
        avg = sum(scores) / len(scores)
        lines.append(f"{category:<22} {avg:4.1f}/10  {'#' * round(avg)}")
    lines.append("=" * 60)
    return "\n".join(lines)


def _interactive_answer(question: Question, index: int) -> str | None:
    print("A (empty line to submit, 'quit' to stop):")
    lines: list[str] = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            return None
        if line.strip().lower() in {"quit", "exit"}:
            return None
        if not line.strip():
            if lines:
                return " ".join(lines)
            continue
        lines.append(line.strip())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Adaptive AI Engineer interview (terminal).")
    parser.add_argument("--level", default="JR", choices=["JR", "MID", "SENIOR"])
    parser.add_argument("--skills", default="", help="comma-separated CV skills")
    parser.add_argument("--questions", type=int, default=8)
    parser.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    parser.add_argument("--semantic", action="store_true", help="use the Chroma index for relevance")
    parser.add_argument("--demo", action="store_true", help="answer automatically with scripted answers")
    args = parser.parse_args(argv)

    service = build_service(bank=args.bank, semantic=args.semantic)
    session = service.start_session(
        starting_level=args.level,
        cv_skills=[s for s in args.skills.split(",") if s.strip()],
        max_questions=args.questions,
    )
    answer_for = demo_answer if args.demo else _interactive_answer
    if args.demo:
        def answer_for(question: Question, index: int) -> str:  # type: ignore[no-redef]
            answer = demo_answer(question, index)
            print(f"A: {answer[:110]}{'...' if len(answer) > 110 else ''}")
            return answer

    session = run(service, session, answer_for)
    print(summary(session))
    return 0


if __name__ == "__main__":
    sys.exit(main())
