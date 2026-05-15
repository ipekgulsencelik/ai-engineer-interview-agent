from __future__ import annotations

from src.domain.evaluation.evaluator import Evaluator
from src.domain.entities.question import Question
from src.domain.results.evaluation_result import EvaluationResult


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

    DEFAULT_SCORE = 7.0
    DEFAULT_FEEDBACK = (
        "Mock evaluation completed successfully."
    )


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
                        score=self.DEFAULT_SCORE,
                        feedback=self.DEFAULT_FEEDBACK,
                        question_id=question.id,    
                        technical_accuracy=7.0,
                        depth=6.0,
                        communication=8.0,
                        missing_keywords=[],
                        follow_up_question=None,
                        confidence=1.0,
                        rubric_version="mock-v1",
                    )

                score:
                    Sabit olarak 7 döner.
                    Bu değer orta-iyi bir aday cevabını simüle eder.

                feedback:
                    Evaluation işleminin mock olarak tamamlandığını belirtir.

                question_id:
                    Değerlendirilen sorunun id değeridir.

                technical_accuracy, depth, communication:
                    Değerlendirme kriterlerine göre sabit puanlar döner.

                missing_keywords:
                    Boş liste döner. Yani hiçbir anahtar kelimenin eksik olmadığı varsayılır.

                follow_up_question:
                    None döner. Yani takip sorusu olmadığı varsayılır.

                confidence:
                    1.0 döner. Yani evaluator'ın değerlendirmeye tamamen güvendiği varsayılır.

                rubric_version:
                    "mock-v1" döner. Yani bu değerlendirme sonucunun mock olduğunu belirtir.

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
 
        self._validate_answer(answer)

        _ = question  # question parametresi kullanılıyor gibi görünmese de, question.id bilgisi response içine eklenir. 
        # Bu yüzden parametre olarak alınır.

        return EvaluationResult(
            score=self.DEFAULT_SCORE,
            feedback=self.DEFAULT_FEEDBACK,
            technical_accuracy=7.0,
            depth=6.0,
            communication=8.0,
            missing_keywords=[],
            follow_up_question=None,
            confidence=1.0,
            rubric_version="mock-v1",
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
    