from __future__ import annotations

from functools import cached_property

from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.application.services.level_transition_service import (
    LevelTransitionService,
)
from src.application.services.question_retrieval_service import (
    QuestionRetrievalService,
)
from src.application.services.question_selection_service import (
    QuestionSelectionService,
)
from src.application.use_cases.run_interview_step_use_case import (
    RunInterviewStepUseCase,
)
from src.domain.policies.cv_gap_score_policy import CvGapScorePolicy
from src.domain.policies.difficulty_score_policy import DifficultyScorePolicy
from src.domain.policies.diversity_score_policy import DiversityScorePolicy
from src.domain.policies.fatigue_score_policy import FatigueScorePolicy
from src.domain.policies.level_score_policy import LevelScorePolicy
from src.domain.policies.market_score_policy import MarketScorePolicy
from src.domain.policies.weighted_scoring_policy import WeightedScoringPolicy
from src.domain.scoring.final_score_calculator import FinalScoreCalculator
from src.domain.scoring.weighted_scoring_engine import WeightedScoringEngine
from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.evaluators.mock_evaluator import MockEvaluator
from src.application.policies.highest_score_selection_policy import (
    HighestScoreSelectionPolicy,
)
from src.infrastructure.vector_stores.question_chrome.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)


class ServiceContainer:
    """
    Application dependency composition root.

    Bu sınıf:
        - concrete dependency wiring yapar
        - singleton lifecycle sağlar
        - route katmanını infrastructure detaylarından izole eder
    """

    @cached_property
    def embedding_provider(
        self,
    ) -> SentenceTransformerEmbeddingProvider:
        return SentenceTransformerEmbeddingProvider()

    @cached_property
    def vector_store(
        self,
    ) -> ChromaQuestionVectorStore:
        return ChromaQuestionVectorStore(
            persist_directory="data/chroma",
        )

    @cached_property
    def question_retrieval_service(
        self,
    ) -> QuestionRetrievalService:
        return QuestionRetrievalService(
            embedding_provider=self.embedding_provider,
            vector_store=self.vector_store,
        )

    @cached_property
    def scoring_policy(
        self,
    ) -> WeightedScoringPolicy:
        return WeightedScoringPolicy(
            level_score_policy=LevelScorePolicy(),
            market_score_policy=MarketScorePolicy(),
            cv_gap_score_policy=CvGapScorePolicy(),
            difficulty_score_policy=DifficultyScorePolicy(),
            diversity_score_policy=DiversityScorePolicy(),
            fatigue_score_policy=FatigueScorePolicy(),
            final_score_calculator=FinalScoreCalculator(),
        )

    @cached_property
    def scoring_engine(
        self,
    ) -> WeightedScoringEngine:
        return WeightedScoringEngine(
            policy=self.scoring_policy,
        )

    @cached_property
    def question_selection_service(
        self,
    ) -> QuestionSelectionService:
        return QuestionSelectionService(
            scoring_engine=self.scoring_engine,
            selection_policy=HighestScoreSelectionPolicy(),
        )

    @cached_property
    def answer_evaluation_service(
        self,
    ) -> AnswerEvaluationService:
        return AnswerEvaluationService(
            evaluator=MockEvaluator(),
        )

    @cached_property
    def level_transition_service(
        self,
    ) -> LevelTransitionService:
        return LevelTransitionService()

    @cached_property
    def run_interview_step_use_case(
        self,
    ) -> RunInterviewStepUseCase:
        return RunInterviewStepUseCase(
            question_retrieval_service=self.question_retrieval_service,
            question_selection_service=self.question_selection_service,
            answer_evaluation_service=self.answer_evaluation_service,
            level_transition_service=self.level_transition_service,
        )