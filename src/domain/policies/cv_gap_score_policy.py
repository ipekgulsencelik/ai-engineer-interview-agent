from __future__ import annotations

from src.domain.constants.scoring import (
    MIN_SCORE,
    UNKNOWN_SKILL_GAP_SCORE,
)
from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.validators.scoring_policy_input_validator import (
    ScoringPolicyInputValidator,
)


class CvGapScorePolicy:
    """
    CV skill gap scoring policy.
    """

    def compute(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        ScoringPolicyInputValidator.validate(
            question=question,
            context=context,
        )

        question_keywords = self._normalize_terms(
            question.keywords,
        )

        if not question_keywords:
            return MIN_SCORE

        cv_skills = self._normalize_terms(
            context.cv_skills,
        )

        if not cv_skills:
            return UNKNOWN_SKILL_GAP_SCORE

        missing_keywords = self._find_missing_keywords(
            question_keywords=question_keywords,
            cv_skills=cv_skills,
        )

        return self._compute_missing_ratio(
            missing_count=len(missing_keywords),
            total_count=len(question_keywords),
        )

    @staticmethod
    def _normalize_terms(
        terms: list[str],
    ) -> set[str]:
        return {
            normalized
            for term in terms
            if isinstance(term, str)
            if (normalized := term.strip().lower())
        }

    @staticmethod
    def _find_missing_keywords(
        *,
        question_keywords: set[str],
        cv_skills: set[str],
    ) -> set[str]:
        return question_keywords - cv_skills

    @staticmethod
    def _compute_missing_ratio(
        *,
        missing_count: int,
        total_count: int,
    ) -> float:
        if total_count <= 0:
            return MIN_SCORE

        return missing_count / total_count