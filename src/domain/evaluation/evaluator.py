from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.entities.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class Evaluator(ABC):
    """
    Candidate answer evaluation davranışı için abstract contract'tır.

    Bu interface'in temel amacı:
        AnswerEvaluationService gibi üst seviye application service'lerin
        concrete evaluator implementasyonlarına doğrudan bağımlı olmasını
        engellemektir.

    ----------------------------------------------------------------------
    EVALUATOR NEDİR?
    ----------------------------------------------------------------------

    Evaluator:
        Bir candidate cevabını alır ve standart EvaluationResult üretir.

    Bu evaluation farklı şekillerde yapılabilir:

        - deterministic mock logic
        - rule-based scoring
        - Groq LLM evaluator
        - OpenAI evaluator
        - hybrid evaluator
        - rubric-based evaluator

    Ancak tüm implementasyonlar aynı contract'a uymalıdır.

    ----------------------------------------------------------------------
    NEDEN INTERFACE VAR?
    ----------------------------------------------------------------------

    Eğer AnswerEvaluationService doğrudan GroqEvaluator veya
    OpenAIEvaluator gibi concrete class'lara bağımlı olursa:

        - test etmek zorlaşır
        - provider değiştirmek zorlaşır
        - mocking maliyeti artar
        - DIP ihlal edilir
        - service provider detaylarına bağımlı hale gelir

    Bu interface sayesinde service yalnızca şu contract'ı bilir:

        evaluator.evaluate(question, answer)

    Hangi provider'ın kullanıldığı önemli değildir.

    ----------------------------------------------------------------------
    PROVIDER-INDEPENDENT RESULT
    ----------------------------------------------------------------------

    Concrete evaluator ne kullanırsa kullansın:

        - Groq
        - OpenAI
        - mock
        - rule engine

    sonuç olarak standart EvaluationResult döndürmelidir.

    Bu yaklaşım:
        downstream servislerin provider-specific response shape bilmesini
        engeller.

    ----------------------------------------------------------------------
    BU INTERFACE NE YAPAR?
    ----------------------------------------------------------------------

    Bu interface:

        ✔ evaluator contract tanımlar
        ✔ polymorphic evaluator mimarisi sağlar
        ✔ provider detaylarını soyutlar
        ✔ AnswerEvaluationService'i concrete evaluator'dan ayırır

    ----------------------------------------------------------------------
    BU INTERFACE NE YAPMAZ?
    ----------------------------------------------------------------------

    Bu interface:

        ✘ prompt oluşturmaz
        ✘ LLM çağrısı yapmaz
        ✘ provider config bilmez
        ✘ parsing yapmaz
        ✘ persistence işlemi yapmaz
        ✘ scoring algoritması içermez

    Sadece:
        evaluation davranışı için ortak sözleşme tanımlar.
    """

    @abstractmethod
    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        """
        Candidate cevabını değerlendirir ve provider-independent
        EvaluationResult döndürür.

        Her concrete evaluator bu method'u implement etmek zorundadır.

        Args:
            question:
                Değerlendirilecek Question domain entity'si.

            answer:
                Candidate tarafından verilen raw answer text.

        Returns:
            EvaluationResult:
                Standardize edilmiş typed evaluation result.

        Raises:
            TypeError:
                Implementasyona bağlı olarak question veya answer tipi
                geçersizse fırlatılabilir.

            ValueError:
                Implementasyona bağlı olarak answer boşsa veya evaluator
                sonucu geçersizse fırlatılabilir.
        """
        pass