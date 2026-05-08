from src.domain.question.question import Question
from src.domain.results.pipeline_result import PipelineResult
from src.domain.scoring.scoring_context import ScoringContext
from src.services.answer_evaluation_service import AnswerEvaluationService
from src.services.level_transition_service import LevelTransitionService
from src.services.question_selection_service import QuestionSelectionService


class RunInterviewStepUseCase:
    """
    Tek bir interview step orchestration'ını yöneten application use-case.

    Bu class, interview sisteminde bir aday cevabı geldiğinde çalıştırılan
    ana business workflow coordinator'dır.

    Amaç:
        Interview sürecindeki tek bir adımı uçtan uca çalıştırmak.

    Bu use-case şu operasyonları sırasıyla yönetir:
        1. Mevcut context'e göre soru seçimi
        2. Aday cevabının değerlendirilmesi
        3. Skor geçmişinin güncellenmesi
        4. Level transition hesaplanması
        5. Final pipeline result oluşturulması

    Neden UseCase?
        Çünkü bu class tek bir domain servisi değildir.

        Birden fazla application service'i birlikte çalıştırır:
            - QuestionSelectionService
            - AnswerEvaluationService
            - LevelTransitionService

        Bu nedenle görevi:
            business workflow orchestration

        olarak düşünülmelidir.

    Service ile UseCase farkı:
        Service:
            Belirli bir domain/application sorumluluğunu yerine getirir.

        UseCase:
            Kullanıcının veya sistemin başlattığı bir iş akışını yönetir.

    Bu class ne yapar?
        ✔ Soru seçtirir
        ✔ Cevabı değerlendirir
        ✔ Result başarısını kontrol eder
        ✔ EvaluationResult unwrap eder
        ✔ Recent scores listesini günceller
        ✔ Next level hesaplatır
        ✔ PipelineResult döndürür

    Bu class ne yapmaz?
        ✘ Scoring algoritması yazmaz
        ✘ LLM provider çağırmaz
        ✘ Soru repository'sinden veri çekmez
        ✘ Level transition kuralını içermez
        ✘ UI response formatlamaz
        ✘ Database persistence yapmaz

    Mimari konum:
        Presentation Layer:
            CLI / API / UI

                ↓

        Application Use Case:
            RunInterviewStepUseCase

                ↓

        Application Services:
            QuestionSelectionService
            AnswerEvaluationService
            LevelTransitionService

                ↓

        Domain / Interfaces:
            Question
            ScoringContext
            EvaluationResult
            PipelineResult

    Dependency Injection:
        Bu use-case ihtiyaç duyduğu servisleri constructor üzerinden alır.

        Böylece:
            - loose coupling sağlanır
            - testlerde fake servis kullanılabilir
            - orchestration logic izole edilir
            - composition root mantığı korunur

    Result pattern kullanımı:
        AnswerEvaluationService doğrudan EvaluationResult değil,
        Result[EvaluationResult] döndürüyor gibi tasarlanmıştır.

        Bu sayede evaluation failure durumları explicit şekilde yönetilir.

    Önemli tasarım notu:
        Bu use-case şu an başarısız evaluation durumunda ValueError fırlatır.

        Faz ilerledikçe bu davranış:
            - Result[PipelineResult]
            - domain-specific exception
            - API error mapping

        yapısına dönüştürülebilir.

    Gelecekte eklenebilecek sorumluluklar:
        - asked_question_ids update
        - context update result
        - coverage snapshot creation
        - telemetry/logging
        - interview history persistence
        - follow-up question handling
        - retry strategy
        - LangGraph state update
        - async execution
    """

    def __init__(
        self,
        question_selection_service: QuestionSelectionService,
        answer_evaluation_service: AnswerEvaluationService,
        level_transition_service: LevelTransitionService,
    ) -> None:
        """
        RunInterviewStepUseCase instance'ı oluşturur.

        Args:
            question_selection_service:
                Candidate question listesi içerisinden mevcut context'e göre
                en uygun soruyu seçen application service.

            answer_evaluation_service:
                Seçilen soru ve aday cevabı üzerinden evaluation işlemini
                yöneten application service.

            level_transition_service:
                Güncel skor geçmişine göre bir sonraki interview seviyesini
                hesaplayan application service.

        Design Note:
            Constructor injection kullanılması bilinçli bir tercihtir.

            Bu yaklaşım:
                - dependency'leri görünür kılar
                - unit test yazmayı kolaylaştırır
                - servislerin dışarıdan compose edilmesini sağlar
                - hard-coded dependency oluşmasını engeller
        """

        # ---------------------------------------------------------
        # DEPENDENCY INJECTION
        # ---------------------------------------------------------
        # Use-case servisleri kendi içinde oluşturmaz.
        #
        # Böylece orchestration logic:
        #   - somut implementation'lardan ayrılır
        #   - testlerde kolayca mock/fake servislerle çalıştırılır
        self.question_selection_service = question_selection_service
        self.answer_evaluation_service = answer_evaluation_service
        self.level_transition_service = level_transition_service

    def execute(
        self,
        questions: list[Question],
        context: ScoringContext,
        answer: str,
    ) -> PipelineResult:
        """
        Tek bir interview step'ini çalıştırır.

        Bu method, use-case'in ana entry point'idir.

        Akış:
            1. QuestionSelectionService ile soru seçilir.
            2. AnswerEvaluationService ile aday cevabı değerlendirilir.
            3. Evaluation result başarısızsa hata fırlatılır.
            4. Başarılı evaluation unwrap edilir.
            5. Skor geçmişi immutable şekilde genişletilir.
            6. LevelTransitionService ile next level hesaplanır.
            7. PipelineResult döndürülür.

        Args:
            questions:
                Selection yapılabilecek candidate question listesi.

                Bu liste genellikle repository veya retrieval katmanından
                üst katmanda hazırlanıp use-case'e verilir.

            context:
                Mevcut interview state bilgisidir.

                Kullanılan alanlar:
                    - current_level
                    - recent_scores
                    - asked_question_ids
                    - weak_areas
                    - cv_skills

            answer:
                Adayın seçilen question'a verdiği cevaptır.

        Returns:
            PipelineResult:
                Interview step sonucunu temsil eden typed result.

                İçerdiği alanlar:
                    - question
                    - evaluation
                    - next_level

        Raises:
            ValueError:
                Evaluation başarısız olursa veya alt servislerden validation
                hatası gelirse fırlatılabilir.

        Design Note:
            Bu method typed PipelineResult döndürür.

            Dict yerine typed result kullanmak:
                - key typo riskini azaltır
                - IDE desteği sağlar
                - refactor güvenliğini artırır
                - API mapping'i daha kontrollü yapar
        """

        # ---------------------------------------------------------
        # QUESTION SELECTION
        # ---------------------------------------------------------
        # Mevcut interview context'i dikkate alınarak en uygun soru seçilir.
        #
        # QuestionSelectionService:
        #   - asked_question_ids filtresi uygular
        #   - scoring engine ile candidate soruları skorlar
        #   - en uygun Question modelini döndürür
        selected_question = self.question_selection_service.select_question(
            questions=questions,
            context=context,
        )

        # ---------------------------------------------------------
        # ANSWER EVALUATION
        # ---------------------------------------------------------
        # Seçilen soru bağlamında aday cevabı değerlendirilir.
        #
        # AnswerEvaluationService burada Result[EvaluationResult] döndürüyor
        # varsayılmıştır.
        #
        # Bu sayede evaluation başarısızlıkları explicit şekilde taşınır.
        evaluation_result_result = self.answer_evaluation_service.evaluate_answer(
            question=selected_question,
            answer=answer,
        )

        # ---------------------------------------------------------
        # EVALUATION FAILURE HANDLING
        # ---------------------------------------------------------
        # Evaluation başarısızsa pipeline devam etmemelidir.
        #
        # Çünkü score olmadan:
        #   - recent_scores update edilemez
        #   - level transition yapılamaz
        #   - güvenilir PipelineResult oluşturulamaz
        if not evaluation_result_result.success:
            raise ValueError(evaluation_result_result.error)

        # ---------------------------------------------------------
        # SUCCESS RESULT UNWRAP
        # ---------------------------------------------------------
        # Başarılı Result içerisinden EvaluationResult alınır.
        #
        # unwrap() başarısız Result üzerinde çağrılırsa exception fırlatır.
        # Ancak yukarıda success kontrolü yapıldığı için bu noktada güvenlidir.
        evaluation_result = evaluation_result_result.unwrap()

        # ---------------------------------------------------------
        # SCORE HISTORY UPDATE
        # ---------------------------------------------------------
        # Context içerisindeki recent_scores listesi doğrudan mutate edilmez.
        #
        # Bunun yerine yeni bir liste oluşturulur.
        #
        # Neden?
        #   - immutable state yaklaşımına uygundur
        #   - side effect riskini azaltır
        #   - test/debug davranışını daha güvenilir yapar
        updated_scores = [
            *context.recent_scores,
            evaluation_result.score,
        ]

        # ---------------------------------------------------------
        # LEVEL TRANSITION
        # ---------------------------------------------------------
        # Güncellenmiş skor geçmişiyle bir sonraki interview seviyesi
        # hesaplanır.
        #
        # LevelTransitionService:
        #   - son skorları analiz eder
        #   - gerekirse level up/down yapar
        #   - aksi durumda mevcut level'i korur
        next_level = self.level_transition_service.transition(
            current_level=context.current_level,
            recent_scores=updated_scores,
        )

        # ---------------------------------------------------------
        # PIPELINE RESULT CREATION
        # ---------------------------------------------------------
        # Final typed response oluşturulur.
        #
        # Bu result:
        #   - API
        #   - CLI
        #   - UI
        #   - telemetry
        #
        # katmanları tarafından güvenli şekilde kullanılabilir.
        return PipelineResult(
            question=selected_question,
            evaluation=evaluation_result,
            next_level=next_level,
        )
