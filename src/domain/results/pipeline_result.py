from dataclasses import dataclass

from src.domain.enums.level import Level
from src.domain.question.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


@dataclass(frozen=True)
class PipelineResult:
    """
    Interview pipeline çalışmasının final çıktısını temsil eden immutable
    domain model.

    Bu modelin amacı:
        Tek bir interview step'i sonucunda oluşan tüm kritik çıktıları
        standart ve type-safe şekilde temsil etmektir.

    PipelineResult:
        interview orchestration layer'ın response modelidir.

    Yani sistem:
        - soru seçtikten
        - cevabı değerlendirdikten
        - level transition hesapladıktan

    sonra oluşan final snapshot bu model ile taşınır.

    Neden ayrı PipelineResult modeli gerekiyor?
        Çünkü interview pipeline çok adımlı bir orchestration sürecidir.

        Bu süreç sonunda:
            - seçilen soru
            - evaluation sonucu
            - bir sonraki level

        birlikte anlamlıdır.

    Eğer yalnızca dict kullanılırsa:
        - schema consistency kaybolur
        - typo riski oluşur
        - IDE desteği azalır
        - maintainability düşer
        - API contract belirsizleşir

    Typed domain model avantajları:
        ✔ type safety
        ✔ immutable state
        ✔ daha güçlü refactor desteği
        ✔ IDE autocomplete
        ✔ deterministic pipeline state
        ✔ cleaner orchestration contract

    Neden frozen=True?
        Çünkü PipelineResult:
            belirli bir interview step'inin immutable sonucudur.

        Yani:
            - hangi soru seçildi
            - nasıl değerlendirildi
            - hangi level'e geçildi

        bilgisi snapshot olarak korunmalıdır.

        Sonradan mutate edilmesi:
            - inconsistent interview history
            - analytics corruption
            - replay/debugging problemleri
            - nondeterministic behavior

        oluşturabilir.

    PipelineResult hangi alanları içerir?
        question:
            Interview step'inde seçilen soru.

        evaluation:
            Aday cevabının evaluation sonucu.

        next_level:
            Evaluation sonrası oluşan yeni interview seviyesi.

    Kullanım alanları:
        - InterviewPipeline
        - CLI output
        - API response
        - telemetry
        - interview history
        - analytics
        - adaptive interview flow
        - LangGraph state updates

    Mimari yaklaşım:
        PipelineResult:
            orchestration sonucu temsil eder.

        Şunları içermez:
            ✘ scoring engine internals
            ✘ evaluator provider bilgisi
            ✘ raw LLM response
            ✘ persistence metadata
            ✘ transport-specific response formatı

        Çünkü bunlar farklı katmanların sorumluluğudur.

    Bu model neden önemli?
        Çünkü orchestration layer:
            sistemin merkezi coordination noktasıdır.

        PipelineResult:
            bu coordination'ın resmi çıktısıdır.

    Gelecekte eklenebilecek alanlar:
        - selection_result
        - coverage_snapshot
        - updated_context
        - telemetry_metadata
        - follow_up_chain
        - pipeline_latency
        - interview_state_version
        - transition_reason

    Example:
        result = PipelineResult(
            question=question,
            evaluation=evaluation_result,
            next_level=Level.MID,
        )

        print(result.question.text)
        print(result.evaluation.score)
        print(result.next_level)

    Output:
        "Explain vector retrieval."
        8.5
        Level.MID
    """

    # ---------------------------------------------------------
    # SELECTED QUESTION
    # ---------------------------------------------------------
    # Interview pipeline sırasında seçilen Question domain modelidir.
    #
    # Bu soru:
    #   - question selection service
    #   - scoring engine
    #   - adaptive interview logic
    #
    # tarafından belirlenmiş olabilir.
    #
    # Kullanım alanları:
    #   - UI rendering
    #   - interview history
    #   - evaluator context
    #   - telemetry
    #
    # Question modeli:
    #   - category
    #   - level
    #   - difficulty
    #   - market relevance
    #
    # gibi önemli interview metadata'sını içerir.
    question: Question

    # ---------------------------------------------------------
    # EVALUATION RESULT
    # ---------------------------------------------------------
    # Aday cevabının evaluation sonucunu temsil eder.
    #
    # Bu alan:
    #   - score
    #   - feedback
    #   - technical_accuracy
    #   - depth
    #   - communication
    #   - missing_keywords
    #
    # gibi evaluation breakdown bilgilerini içerir.
    #
    # Kullanım alanları:
    #   - candidate feedback
    #   - analytics
    #   - level transition
    #   - adaptive interview logic
    evaluation: EvaluationResult

    # ---------------------------------------------------------
    # NEXT INTERVIEW LEVEL
    # ---------------------------------------------------------
    # Evaluation sonrası oluşan yeni interview seviyesini temsil eder.
    #
    # Bu değer:
    #   LevelTransitionService
    #
    # tarafından hesaplanır.
    #
    # Örnek progression:
    #   JR
    #       ↓
    #   MID
    #       ↓
    #   SENIOR
    #
    # Kullanım alanları:
    #   - next question selection
    #   - adaptive interview flow
    #   - candidate calibration
    #   - progression tracking
    #
    # Enum kullanılması:
    #   - invalid level riskini azaltır
    #   - type safety sağlar
    #   - interview state consistency üretir
    next_level: Level
