from src.domain.entities.question import Question
from src.domain.ranker.ranked_candidate import RankedCandidate
from src.domain.scoring.scoring_context import ScoringContext
from src.interfaces.scoring_engine import ScoringEngine


class CandidateRanker:
    """
    Candidate question ranking işlemini yöneten service.

    Bu sınıfın amacı:
        - candidate question listesini scoring engine ile skorlamak
        - skorlarına göre büyükten küçüğe sıralamak
        - her adaya rank değeri atamak

    Bu sınıf:
        - filtering yapmaz
        - question seçmez
        - result object oluşturmaz
        - scoring algoritmasını bilmez

    Sadece ranking orchestration yapar.
    """

    def __init__(
        self,
        scoring_engine: ScoringEngine,
    ) -> None:
        self.scoring_engine = scoring_engine

    def rank(
        self,
        *,
        questions: list[Question],
        context: ScoringContext,
    ) -> list[RankedCandidate]:
        """
        Candidate soruları skorlar ve ranked candidate listesi döndürür.
        """

        ranked_candidates = [
            RankedCandidate(
                rank=0,
                question=question,
                score=explanation.final_score,
                explanation=explanation,
            )
            for question in questions
            for explanation in [
                self.scoring_engine.score(
                    question=question,
                    context=context,
                )
            ]       
        ]

        sorted_candidates = sorted(
            ranked_candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        return [
            RankedCandidate(
                rank=index,
                question=candidate.question,
                score=candidate.score,
                explanation=candidate.explanation,
            )
            for index, candidate in enumerate(
                sorted_candidates,
                start=1,
            )
        ]