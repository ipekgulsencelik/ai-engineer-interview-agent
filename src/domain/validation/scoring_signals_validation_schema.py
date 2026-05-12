from __future__ import annotations

from typing import Any

from src.domain.interview.adaptive_pacing import AdaptivePacing
from src.domain.interview.interview_coverage import InterviewCoverage
from src.domain.interview.question_fatigue import QuestionFatigue
from src.domain.retrieval.semantic_relevance import SemanticRelevance
from src.domain.scoring.scoring_weights import ScoringWeights


SCORING_SIGNALS_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "coverage": {
        "type": InterviewCoverage,
        "nullable": True,
    },
    "fatigue": {
        "type": QuestionFatigue,
        "nullable": True,
    },
    "semantic_relevance": {
        "type": SemanticRelevance,
        "nullable": True,
    },
    "adaptive_pacing": {
        "type": AdaptivePacing,
        "nullable": True,
    },
    "weights": {
        "type": ScoringWeights,
        "nullable": True,
    },
}