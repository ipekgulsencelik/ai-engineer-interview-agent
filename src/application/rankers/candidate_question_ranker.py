from __future__ import annotations

from src.application.ports.scoring_engine import ScoringEngine
from src.application.services.ranking.candidate_question_ranker_validator import (
    CandidateQuestionRankerValidator,
)
from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext
from src.domain.selection.ranked_candidate import RankedCandidate
from src.domain.selection.scored_candidate import ScoredCandidate


class CandidateQuestionRanker:
    """
    Scores candidate questions and assigns rank by descending score.
    """

    def __init__(
        self,
        scoring_engine: ScoringEngine,
    ) -> None:
        CandidateQuestionRankerValidator.validate_scoring_engine(
            scoring_engine,
        )

        self._scoring_engine = scoring_engine

    def rank(
        self,
        *,
        questions: list[Question],
        context: ScoringContext,
    ) -> list[RankedCandidate]:
        CandidateQuestionRankerValidator.validate_questions(
            questions,
        )
        CandidateQuestionRankerValidator.validate_context(
            context,
        )

        if not questions:
            return []

        scored_candidates = self._score_candidates(
            questions=questions,
            context=context,
        )

        sorted_candidates = self._sort_by_score_desc(
            candidates=scored_candidates,
        )

        return self._assign_ranks(
            candidates=sorted_candidates,
        )

    def _score_candidates(
        self,
        *,
        questions: list[Question],
        context: ScoringContext,
    ) -> list[ScoredCandidate]:
        scored_candidates: list[ScoredCandidate] = []

        for question in questions:
            breakdown = self._scoring_engine.score(
                question=question,
                context=context,
            )

            scored_candidates.append(
                ScoredCandidate(
                    question=question,
                    score=breakdown.final_score,
                    breakdown=breakdown,
                )
            )

        return scored_candidates

    @staticmethod
    def _sort_by_score_desc(
        *,
        candidates: list[ScoredCandidate],
    ) -> list[ScoredCandidate]:
        return sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

    @staticmethod
    def _assign_ranks(
        *,
        candidates: list[ScoredCandidate],
    ) -> list[RankedCandidate]:
        return [
            RankedCandidate(
                rank=index,
                question=candidate.question,
                score=candidate.score,
                breakdown=candidate.breakdown,
            )
            for index, candidate in enumerate(
                candidates,
                start=1,
            )
        ]