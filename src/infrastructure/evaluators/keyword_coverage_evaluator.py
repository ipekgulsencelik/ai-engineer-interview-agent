"""Offline, deterministic answer evaluator based on rubric coverage.

Used when no LLM evaluator is configured (no GROQ_API_KEY), in tests and in
the terminal demo. It is a transparent heuristic, not a replacement for the
LLM rubric evaluator: it rewards answers that mention the question's keywords
and expected points, and that are developed enough to show depth.

Score composition mirrors the rubric weights in DECISIONS.md (decision 9):
technical accuracy 40%, depth 35%, communication 25%.
"""

from __future__ import annotations

import re

from src.domain.entities.question import Question
from src.domain.evaluation.evaluator import Evaluator
from src.domain.metadata.evaluation_metadata import EvaluationMetadata
from src.domain.results.evaluation_result import EvaluationResult

RUBRIC_VERSION = "keyword-coverage-v1"
TECHNICAL_WEIGHT = 0.40
DEPTH_WEIGHT = 0.35
COMMUNICATION_WEIGHT = 0.25

# Words carrying no technical signal when matching expected points.
_STOPWORDS = frozenset(
    "a an and are as at be by for from how in into is it its of on or "
    "the their them then to via what when which with without".split()
)
_WORD = re.compile(r"[a-z0-9][a-z0-9+\-]*")


def _terms(text: str) -> set[str]:
    return {
        _stem(word)
        for word in _WORD.findall(text.lower())
        if word not in _STOPWORDS and len(word) > 2
    }


def _stem(word: str) -> str:
    for suffix in ("ings", "ing", "ies", "es", "s", "ed"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)]
    return word


def _covered(phrase: str, answer_terms: set[str]) -> bool:
    """A phrase counts as covered when most of its content words appear."""
    phrase_terms = _terms(phrase)
    if not phrase_terms:
        return False
    hits = sum(1 for term in phrase_terms if _matches(term, answer_terms))
    return hits / len(phrase_terms) >= 0.5


def _matches(term: str, answer_terms: set[str]) -> bool:
    """Exact match, or a shared prefix of 6+ chars (retrieval ~ retrieves)."""
    if term in answer_terms:
        return True
    if len(term) < 6:
        return False
    prefix = term[:6]
    return any(word.startswith(prefix) for word in answer_terms)


class KeywordCoverageEvaluator(Evaluator):
    """Scores answers 0-10 by keyword/expected-point coverage and development."""

    def evaluate(self, *, question: Question, answer: str) -> EvaluationResult:
        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        answer_terms = _terms(answer)
        keywords = list(question.keywords)
        points = list(question.expected_points)

        missing_keywords = tuple(k for k in keywords if not _covered(k, answer_terms))
        covered_points = [p for p in points if _covered(p, answer_terms)]

        keyword_ratio = 1 - len(missing_keywords) / len(keywords) if keywords else 0.0
        point_ratio = len(covered_points) / len(points) if points else keyword_ratio

        technical = 10 * (0.5 * keyword_ratio + 0.5 * point_ratio)

        word_count = len(_WORD.findall(answer.lower()))
        # Depth: needs both coverage and a developed explanation (~60+ words).
        development = min(word_count / 60, 1.0)
        depth = 10 * point_ratio * (0.4 + 0.6 * development)

        sentences = [s for s in re.split(r"[.!?]+", answer) if s.strip()]
        communication = 10 * min(len(sentences) / 3, 1.0) * (0.5 + 0.5 * development)

        score = round(
            TECHNICAL_WEIGHT * technical
            + DEPTH_WEIGHT * depth
            + COMMUNICATION_WEIGHT * communication,
            1,
        )

        return EvaluationResult(
            score=score,
            feedback=self._feedback(points, covered_points, missing_keywords),
            technical_accuracy=round(technical, 1),
            depth=round(depth, 1),
            communication=round(communication, 1),
            metadata=EvaluationMetadata(
                confidence=0.5,
                rubric_version=RUBRIC_VERSION,
                missing_keywords=missing_keywords,
                follow_up_question=question.followup,
            ),
        )

    @staticmethod
    def _feedback(
        points: list[str],
        covered_points: list[str],
        missing_keywords: tuple[str, ...],
    ) -> str:
        missed = [p for p in points if p not in covered_points]
        if not missed and not missing_keywords:
            return "Covers all expected points."
        parts = [f"Covered {len(covered_points)}/{len(points)} expected points."]
        if missed:
            parts.append("Missing: " + "; ".join(missed[:3]) + ".")
        if missing_keywords:
            parts.append("Consider mentioning: " + ", ".join(missing_keywords[:4]) + ".")
        return " ".join(parts)
