from __future__ import annotations

from src.domain.evaluation.evaluator import Evaluator
from src.domain.entities.question import Question
from src.domain.metadata.evaluation_metadata import EvaluationMetadata
from src.domain.results.evaluation_result import EvaluationResult


class MockEvaluator(Evaluator):

    DEFAULT_SCORE = 7.0
    DEFAULT_FEEDBACK = (
        "Mock evaluation completed successfully."
    )


    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
 
        self._validate_answer(answer)

        _ = question  # question parametresi kullanılıyor gibi görünmese de, question.id bilgisi response içine eklenir. 
        # Bu yüzden parametre olarak alınır.

        return EvaluationResult(
            score=self.DEFAULT_SCORE,
            feedback=self.DEFAULT_FEEDBACK,
            technical_accuracy=7.0,
            depth=6.0,
            communication=8.0,
            metadata=EvaluationMetadata(
                confidence=1.0,
                rubric_version="mock-v1",
                missing_keywords=(),
                follow_up_question=None,
            ),
        )


    @staticmethod
    def _validate_answer(
        answer: str,
    ) -> None:
        """
        Evaluator-level semantic validation.

        Bu method, evaluate(...) metoduna gelen answer parametresinin
        geçerli bir string olduğunu doğrular.
        """

        if not answer.strip():
            raise ValueError("Answer cannot be empty.")
    