from src.domain.question.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)
from src.interfaces.evaluator import Evaluator


class MockEvaluator(Evaluator):
    """
    Test ve local development için kullanılan sahte evaluator.

    Bu sınıf gerçek bir LLM provider çağrısı yapmaz.
    Yani Groq, OpenAI, Anthropic veya başka bir external API ile iletişime
    geçmez.

    Amaç:
        Evaluation pipeline'ını dış bağımlılıklardan izole ederek test
        edilebilir hale getirmektir.

    MockEvaluator özellikle şu durumlarda kullanılır:
        - unit test yazarken
        - local development sırasında
        - LLM API key olmadan sistemi çalıştırırken
        - evaluation service davranışını hızlı test ederken
        - pipeline entegrasyonunu doğrularken
        - maliyet oluşturmadan demo akışı çalıştırırken

    Neden MockEvaluator gerekli?
        Gerçek LLM evaluator kullanıldığında sistem:
            - API key ister
            - internet bağlantısına ihtiyaç duyar
            - response süresi değişken olur
            - token maliyeti oluşturur
            - output bazen nondeterministic olabilir
            - testler yavaş ve kırılgan hale gelebilir

        MockEvaluator bu sorunları ortadan kaldırır.

    Bu sınıf sayesinde:
        - AnswerEvaluationService test edilebilir.
        - InterviewPipeline uçtan uca çalıştırılabilir.
        - LevelTransitionService için skor senaryoları denenebilir.
        - UI veya CLI demo akışı hızlıca doğrulanabilir.
        - CI ortamında external provider bağımlılığı olmadan test koşulabilir.

    Mimari konum:
        Interface:
            Evaluator

        Concrete test/local implementation:
            MockEvaluator

        Kullanıldığı yerler:
            - AnswerEvaluationService
            - InterviewPipeline
            - local CLI demo
            - unit/integration tests

    Tasarım notu:
        MockEvaluator, Evaluator interface'ini implemente eder.
        Bu sayede gerçek evaluator ile aynı contract'a sahiptir.

        Yani AnswerEvaluationService açısından:
            MockEvaluator
            GroqEvaluator
            OpenAIEvaluator

        arasında fark yoktur.

        Service yalnızca evaluate(...) metodunu çağırır.

    Önemli:
        Bu sınıf production-grade gerçek değerlendirme yapmaz.
        Döndürdüğü skor sabittir ve sadece pipeline davranışını test etmek
        içindir.

    Not:
        İleride daha gelişmiş test senaryoları için:
            - ConfigurableMockEvaluator
            - ScoreSequenceMockEvaluator
            - KeywordBasedFakeEvaluator

        gibi farklı fake/mock evaluator'lar eklenebilir.
    """

    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        """
        Aday cevabı için deterministic mock evaluation sonucu döndürür.

        Bu method gerçek bir LLM çağrısı yapmaz.
        Bunun yerine sabit ve tahmin edilebilir bir response üretir.

        Args:
            question:
                Değerlendirilecek Question domain modelidir.

                Bu modelden özellikle question.id bilgisi response içerisine
                eklenir. Böylece testlerde hangi sorunun değerlendirildiği
                kolayca doğrulanabilir.

            answer:
                Adayın verdiği ham cevaptır.

                Boş cevap kabul edilmez.
                Çünkü gerçek evaluator'larda da boş cevap değerlendirmek
                anlamlı değildir.

        Returns:
            EvaluationResult:
                Mock evaluation sonucunu temsil eden EvaluationResult nesnesi.

                Dönen örnek yapı:
                    EvaluationResult(
                        score=7,
                        feedback="Mock evaluation completed successfully.",
                        question_id="rag_jr_001",
                    )

                score:
                    Sabit olarak 7 döner.
                    Bu değer orta-iyi bir aday cevabını simüle eder.

                feedback:
                    Evaluation işleminin mock olarak tamamlandığını belirtir.

                question_id:
                    Değerlendirilen sorunun id değeridir.

        Raises:
            ValueError:
                answer boş veya sadece whitespace karakterlerinden oluşuyorsa
                fırlatılır.

        Design Note:
            Bu methodun deterministic olması bilinçli bir tercihtir.

            Çünkü testlerde aynı input için her zaman aynı output alınmalıdır.
            Bu, test güvenilirliğini artırır.

            Gerçek LLM evaluator'larda output değişken olabilir.
            MockEvaluator ise bu değişkenliği ortadan kaldırır.
        """

        # ---------------------------------------------------------
        # ANSWER VALIDATION
        # ---------------------------------------------------------
        # Boş cevap değerlendirme için anlamlı değildir.
        #
        # strip() kullanmamızın nedeni:
        #   "   " gibi sadece boşluklardan oluşan cevapları da geçersiz
        #   kabul etmektir.
        #
        # Bu validation gerçek evaluator davranışına da yakındır.
        if not answer.strip():
            raise ValueError("Answer cannot be empty.")

        # ---------------------------------------------------------
        # DETERMINISTIC MOCK RESPONSE
        # ---------------------------------------------------------
        # Burada sabit bir skor döndürüyoruz.
        #
        # Neden sabit?
        #   - unit testlerde predictable sonuç üretmek için
        #   - LLM provider'a bağlı kalmamak için
        #   - pipeline entegrasyonunu hızlıca doğrulamak için
        #
        # Bu sonuç gerçek aday performansını ölçmez.
        # Sadece sistemin evaluation flow'unun çalıştığını gösterir.
        return EvaluationResult(
            score=7,
            feedback="Mock evaluation completed successfully.",
        )
