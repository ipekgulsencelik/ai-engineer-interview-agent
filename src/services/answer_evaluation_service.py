from src.domain.common.result import Result
from src.domain.question.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)
from src.interfaces.evaluator import Evaluator


class AnswerEvaluationService:
    """
    Aday cevabının değerlendirilmesini yöneten application service.

    Bu service'in temel sorumluluğu:
        - aday cevabını almak
        - gerekli validation işlemlerini yapmak
        - uygun evaluator'a delegasyon yapmak
        - evaluation sonucunu döndürmektir

    Bu service doğrudan:
        - Groq SDK
        - OpenAI SDK
        - Anthropic API
        - prompt engineering logic
        - HTTP request logic

    bilmez.

    Bunun yerine yalnızca Evaluator abstraction'ına bağımlıdır.

    Bu yaklaşım sayesinde service:
        - provider bağımsız kalır
        - test edilebilir hale gelir
        - infrastructure detaylarından izole edilir
        - SOLID prensiplerine uygun olur

    Neden service katmanı kullanıyoruz?
        Çünkü evaluation işlemi application seviyesinde bir use-case'tir.

        Domain model:
            Sadece veri ve kuralları temsil eder.

        Evaluator:
            Teknik evaluation implementasyonudur.

        Service:
            Use-case orchestration yapar.

    Mimari konum:
        Presentation layer:
            CLI / API / UI

                ↓

        Application layer:
            AnswerEvaluationService

                ↓

        Interface:
            Evaluator

                ↓

        Infrastructure layer:
            GroqEvaluator
            OpenAIEvaluator
            MockEvaluator

    Dependency Injection:
        Evaluator constructor üzerinden inject edilir.

        Böylece:
            - Loose coupling sağlanır
            - Testlerde mock kullanılabilir
            - Provider değiştirmek kolaylaşır

    Örnek:
        service = AnswerEvaluationService(
            evaluator=GroqEvaluator(...)
        )

    Test örneği:
        service = AnswerEvaluationService(
            evaluator=MockEvaluator()
        )

    Bu yaklaşımın avantajları:
        ✔ Dependency Inversion Principle uygulanır
        ✔ Test edilebilirlik artar
        ✔ Mock/Fake evaluator kolay kullanılır
        ✔ Infrastructure değişiklikleri service'i bozmaz
        ✔ Service sadece orchestration yapar

    Önemli tasarım notu:
        Bu service scoring algoritmasını içermez.
        Aynı şekilde prompt generation logic de burada olmamalıdır.

        Çünkü:
            - scoring evaluator sorumluluğudur
            - prompt engineering evaluator veya prompt builder katmanına aittir

    Bu service yalnızca:
        - validation
        - orchestration
        - delegasyon

    yapmalıdır.

    İleride bu service genişletilebilir:
        - evaluation caching
        - telemetry
        - evaluation logging
        - retry mekanizması
        - async processing
        - evaluation history
        - analytics
        - feedback enrichment

    gibi özellikler eklenebilir.
    """

    def __init__(self, evaluator: Evaluator) -> None:
        """
        AnswerEvaluationService instance'ı oluşturur.

        Args:
            evaluator:
                Aday cevabını değerlendirecek evaluator implementasyonudur.

                Bu parametre doğrudan somut provider'a değil,
                Evaluator abstraction'ına bağlıdır.

                Örnek implementasyonlar:
                    - MockEvaluator
                    - GroqEvaluator
                    - OpenAIEvaluator
                    - RuleBasedEvaluator

        Design Note:
            Constructor injection kullanılması bilinçli bir tercihtir.

            Böylece:
                - dependency açık şekilde görünür
                - test yazımı kolaylaşır
                - service lifecycle daha kontrollü olur
                - hidden dependency oluşmaz

        Example:
            evaluator = MockEvaluator()

            service = AnswerEvaluationService(
                evaluator=evaluator
            )
        """

        # ---------------------------------------------------------
        # DEPENDENCY INJECTION
        # ---------------------------------------------------------
        # Service evaluator implementasyonunu doğrudan oluşturmaz.
        #
        # Böylece:
        #   - loose coupling korunur
        #   - provider bağımlılığı azalır
        #   - mock/fake evaluator kolay kullanılabilir
        self.evaluator = evaluator

    def evaluate_answer(
        self,
        question: Question,
        answer: str,
    ) -> Result[EvaluationResult]:
        """
        Aday cevabını değerlendirir.

        Bu method application-level evaluation use-case'ini temsil eder.

        Akış:
            1. Input validation yapılır.
            2. Evaluator'a delegasyon yapılır.
            3. Evaluation sonucu döndürülür.

        Bu service evaluation algoritmasını kendisi implemente etmez.
        Yalnızca orchestration görevi görür.

        Args:
            question:
                Adaya sorulan Question domain modelidir.

                Bu model:
                    - soru metni
                    - category
                    - level
                    - expected points
                    - keywords
                gibi evaluator için gerekli context bilgisini içerir.

            answer:
                Adayın verdiği ham text cevaptır.

                Bu değer:
                    - boş olmamalıdır
                    - whitespace-only olmamalıdır

        Returns:
            Result[EvaluationResult]:
                Evaluator tarafından üretilen evaluation sonucudur.

                Örnek:
                    Result(
                        success=True,
                        data=EvaluationResult(
                            score=8,
                            feedback="Good understanding of embeddings.",
                            missing_keywords=["vector similarity"],
                        ),
                        error=None
                    )

                Dönen yapı evaluator implementasyonuna göre genişleyebilir.

        Raises:
            ValueError:
                answer boş veya yalnızca whitespace karakterlerinden oluşuyorsa
                fırlatılır.

            RuntimeError:
                Evaluator implementasyonu external API veya provider kaynaklı
                hata üretirse üst katmana propagate edilebilir.

        Design Note:
            Validation'ın service katmanında yapılması bilinçlidir.

            Böylece:
                - evaluator daha temiz kalır
                - invalid request erken yakalanır
                - application boundary korunur

            Ancak kritik domain validation'lar yine evaluator veya domain
            seviyesinde de yapılabilir.

        Example:
            result = service.evaluate_answer(
                question=question,
                answer="RAG combines retrieval and generation."
            )

            print(result.unwrap().score)
        """

        # ---------------------------------------------------------
        # ANSWER VALIDATION
        # ---------------------------------------------------------
        # Boş cevap evaluation için anlamlı değildir.
        #
        # strip() kullanmamızın nedeni:
        #   "   " gibi yalnızca whitespace içeren cevapları da
        #   geçersiz kabul etmektir.
        #
        # Validation'ı burada yapmak:
        #   - invalid request'i erken yakalamamızı sağlar
        #   - evaluator implementasyonunu sade tutar
        if not answer.strip():
            return Result.fail("Answer cannot be empty.")

        # ---------------------------------------------------------
        # EVALUATION DELEGATION
        # ---------------------------------------------------------
        # Gerçek evaluation logic evaluator implementasyonuna bırakılır.
        #
        # Bu service:
        #   - scoring algoritmasını bilmez
        #   - provider SDK'sını bilmez
        #   - prompt engineering bilmez
        #
        # Sadece orchestration yapar.
        #
        # Böylece service:
        #   - provider bağımsız
        #   - test edilebilir
        #   - genişletilebilir
        # hale gelir.
        try:
            evaluation_result = self.evaluator.evaluate(
                question=question,
                answer=answer,
            )

            return Result.ok(evaluation_result)

        except Exception as exc:
            return Result.fail(str(exc))
