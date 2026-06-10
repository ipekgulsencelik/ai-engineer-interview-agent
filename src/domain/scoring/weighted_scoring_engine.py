from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from src.application.ports.scoring_engine import (
    ScoringEngine,
)
from src.domain.entities.question import Question
from src.domain.policies.weighted_scoring_policy import (
    WeightedScoringPolicy,
)
from src.domain.results.selection_breakdown import (
    SelectionBreakdown,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.validators.weighted_scoring_engine_validator import (
    WeightedScoringEngineValidator,
)


@dataclass(frozen=True)
class _ScoreComponent:
    """Single-responsibility score computation descriptor."""

    name: str
    compute: Callable[[Question, ScoringContext], float]


class WeightedScoringEngine(ScoringEngine):
    """
    Weighted explainable scoring engine.
    """

    def __init__(
        self,
        policy: WeightedScoringPolicy,
    ) -> None:
        WeightedScoringEngineValidator.validate_policy(
            policy,
        )

        self._policy = policy
        self._components = self._build_score_components()

    def score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> SelectionBreakdown:
        WeightedScoringEngineValidator.validate_input(
            question=question,
            context=context,
        )

        component_scores = self._compute_component_scores(
            question=question,
            context=context,
        )

        final_score = self._policy.compute_final_score(
            level_score=component_scores["level_score"],
            market_score=component_scores["market_score"],
            cv_gap_score=component_scores["cv_gap_score"],
            difficulty_score=component_scores["difficulty_score"],
            diversity_score=component_scores["diversity_score"],
            fatigue_score=component_scores["fatigue_score"],
        )

        return SelectionBreakdown(
            level_score=component_scores["level_score"],
            market_score=component_scores["market_score"],
            cv_gap_score=component_scores["cv_gap_score"],
            difficulty_score=component_scores["difficulty_score"],
            diversity_score=component_scores["diversity_score"],
            fatigue_score=component_scores["fatigue_score"],
            final_score=final_score,
        )

    def _build_score_components(self) -> tuple[_ScoreComponent, ...]:
        return (
            _ScoreComponent(
                name="level_score",
                compute=lambda question, context: self._policy.compute_level_score(
                    question=question,
                    context=context,
                ),
            ),
            _ScoreComponent(
                name="market_score",
                compute=lambda question, context: self._policy.compute_market_score(
                    question=question,
                    context=context,
                ),
            ),
            _ScoreComponent(
                name="cv_gap_score",
                compute=lambda question, context: self._policy.compute_cv_gap_score(
                    question=question,
                    context=context,
                ),
            ),
            _ScoreComponent(
                name="difficulty_score",
                compute=lambda question, context: self._policy.compute_difficulty_score(
                    question=question,
                    context=context,
                ),
            ),
            _ScoreComponent(
                name="diversity_score",
                compute=lambda question, context: self._policy.compute_diversity_score(
                    question=question,
                    context=context,
                ),
            ),
            _ScoreComponent(
                name="fatigue_score",
                compute=lambda question, context: self._policy.compute_fatigue_score(
                    question=question,
                    context=context,
                ),
            ),
        )

    def _compute_component_scores(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> dict[str, float]:
        return {
            component.name: component.compute(
                question,
                context,
            )
            for component in self._components
        }