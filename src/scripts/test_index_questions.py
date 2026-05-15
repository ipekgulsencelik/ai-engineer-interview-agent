from __future__ import annotations

from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.application.services.level_transition_service import (
    LevelTransitionService,
)
from src.services.question_retrieval_service import (
    QuestionRetrievalService,
)
from src.services.question_selection_service import (
    QuestionSelectionService,
)
from src.application.use_cases.run_interview_step import (
    RunInterviewStep,
)
from src.domain.policies.cv_gap_score_policy import (
    CvGapScorePolicy,
)
from src.domain.policies.difficulty_score_policy import (
    DifficultyScorePolicy,
)
from src.domain.policies.diversity_score_policy import (
    DiversityScorePolicy,
)
from src.domain.policies.fatigue_score_policy import (
    FatigueScorePolicy,
)
from src.domain.policies.level_score_policy import (
    LevelScorePolicy,
)
from src.domain.policies.market_score_policy import (
    MarketScorePolicy,
)
from src.domain.policies.weighted_scoring_policy import (
    WeightedScoringPolicy,
)
from src.domain.scoring.final_score_calculator import (
    FinalScoreCalculator,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.scoring.weighted_scoring_engine import (
    WeightedScoringEngine,
)
from src.infrastructure.embeddings.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.evaluators.mock_evaluator import (
    MockEvaluator,
)
from src.infrastructure.vectorstores.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)


def build_use_case() -> RunInterviewStepUseCase:
    embedding_provider = (
        SentenceTransformerEmbeddingProvider()
    )

    vector_store = ChromaQuestionVectorStore(
        persist_directory="data/chroma",
    )

    retrieval_service = (
        QuestionRetrievalService(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )
    )

    policy = WeightedScoringPolicy(
        level_score_policy=LevelScorePolicy(),
        market_score_policy=MarketScorePolicy(),
        cv_gap_score_policy=CvGapScorePolicy(),
        difficulty_score_policy=DifficultyScorePolicy(),
        diversity_score_policy=DiversityScorePolicy(),
        fatigue_score_policy=FatigueScorePolicy(),
        final_score_calculator=(
            FinalScoreCalculator()
        ),
    )

    scoring_engine = WeightedScoringEngine(
        policy=policy,
    )

    selection_service = (
        QuestionSelectionService(
            candidate_filter=None,  # replace later
            candidate_ranker=None,  # replace later
            selection_policy=None,  # replace later
        )
    )

    evaluation_service = (
        AnswerEvaluationService(
            evaluator=MockEvaluator(),
        )
    )

    transition_service = (
        LevelTransitionService()
    )

    return RunInterviewStepUseCase(
        question_selection_service=selection_service,
        answer_evaluation_service=evaluation_service,
        level_transition_service=transition_service,
    )


def main() -> None:
    use_case = build_use_case()

    context = ScoringContext()

    print(
        "\n=== AI Interview Demo ===\n"
    )

    # temporary mock question list
    questions = []

    answer = input(
        "Candidate Answer:\n> "
    )

    result = use_case.execute(
        questions=questions,
        context=context,
        answer=answer,
    )

    print("\n=== RESULT ===\n")

    print(
        f"Question:\n"
        f"{result.selection_result.selected_question.text}\n"
    )

    print(
        f"Score: "
        f"{result.evaluation_result.score}"
    )

    print(
        f"Feedback:\n"
        f"{result.evaluation_result.feedback}\n"
    )

    print(
        f"Next Level: "
        f"{result.next_level.value}"
    )


if __name__ == "__main__":
    main()