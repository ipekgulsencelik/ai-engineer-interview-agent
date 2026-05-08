import json

from groq import Groq

from src.config.settings import settings
from src.domain.question.question import Question
from src.domain.results.follow_up_result import (
    FollowUpResult,
)
from src.logging.logger import logger


class FollowUpGenerationService:
    """
    Adaptive follow-up question generation service.

    Bu service'in amacı:
        Candidate answer'a göre dinamik, context-aware ve teknik açıdan
        derinleştirici follow-up question üretmektir.

    Interview sistemlerinde neden follow-up generation gerekir?
        Çünkü statik soru akışları:
            - yüzeysel değerlendirme yapabilir
            - candidate reasoning depth'ini kaçırabilir
            - gerçek teknik hakimiyeti ölçemeyebilir

    Adaptive follow-up yaklaşımı sayesinde:
        ✔ interview daha doğal olur
        ✔ reasoning depth ölçülebilir
        ✔ weak area probing yapılabilir
        ✔ shallow answer detection mümkün olur
        ✔ conversational interview flow oluşur

    Bu service nasıl çalışır?
        1. Original question alınır.
        2. Candidate answer analiz edilir.
        3. Missing concepts belirlenir.
        4. Teknik derinlik eksikleri analiz edilir.
        5. LLM üzerinden intelligent follow-up üretilir.
        6. Sonuç FollowUpResult domain modeline dönüştürülür.

    Bu service ne yapar?
        ✔ follow-up generation
        ✔ prompt construction
        ✔ Groq LLM orchestration
        ✔ JSON parsing
        ✔ FollowUpResult mapping

    Bu service ne yapmaz?
        ✘ answer evaluation
        ✘ question selection
        ✘ level transition
        ✘ retrieval
        ✘ scoring
        ✘ persistence

    Mimari konum:
        Application Service:
            FollowUpGenerationService

        Infrastructure:
            Groq SDK

        Domain:
            FollowUpResult
            Question

    Önemli mimari not:
        Bu class şu an doğrudan Groq SDK'sına bağımlıdır.

        Daha clean architecture yaklaşımında:
            LLMClient abstraction

        kullanılması daha uygundur.

    Örnek:
        FollowUpGenerationService(
            llm_client: LLMClient
        )

    Böylece:
        ✔ OpenAI
        ✔ Anthropic
        ✔ local model
        ✔ mock client

        kolayca değiştirilebilir.

    Şu anki implementasyon Faz-1 için yeterlidir.

    response_format neden önemli?
        Çünkü model çıktısı:
            deterministic JSON

        olmalıdır.

        Aksi halde:
            json.loads()

        parsing problemleri oluşabilir.

    Gelecekte eklenebilecek geliştirmeler:
        - multi-step follow-up chains
        - category-aware probing
        - difficulty-adaptive follow-ups
        - retry strategy
        - prompt versioning
        - telemetry
        - chain-of-thought scoring
        - semantic grounding
        - hallucination detection
    """

    def __init__(self) -> None:
        """
        FollowUpGenerationService instance'ı oluşturur.

        Bu aşamada:
            - API key validation yapılır
            - Groq client initialize edilir
            - kullanılacak model belirlenir

        Raises:
            ValueError:
                GROQ_API_KEY tanımlı değilse fırlatılır.
        """

        # ---------------------------------------------------------
        # API KEY VALIDATION
        # ---------------------------------------------------------
        # Gerçek provider çağrısı yapılacağı için API key zorunludur.
        #
        # Eksik olması durumunda service çalışamaz.
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing.")

        # ---------------------------------------------------------
        # GROQ CLIENT INITIALIZATION
        # ---------------------------------------------------------
        # Groq SDK client oluşturulur.
        #
        # Bu client:
        #   follow-up generation inference
        #
        # için kullanılacaktır.
        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        # ---------------------------------------------------------
        # MODEL CONFIGURATION
        # ---------------------------------------------------------
        # Kullanılacak LLM modeli centralized settings üzerinden alınır.
        #
        # Böylece model switching:
        #   config-level
        #
        # hale gelir.
        self.model = settings.GROQ_MODEL_NAME

    def generate(
        self,
        question: Question,
        answer: str,
    ) -> FollowUpResult:
        """
        Candidate answer'a göre adaptive follow-up question üretir.

        Akış:
            1. Answer validation yapılır.
            2. Prompt oluşturulur.
            3. Groq LLM çağrısı yapılır.
            4. JSON response parse edilir.
            5. FollowUpResult oluşturulur.

        Args:
            question:
                Original interview question domain modeli.

                Kullanılan alanlar:
                    - text
                    - expected_points
                    - category
                    - difficulty

            answer:
                Candidate'ın verdiği cevap.

        Returns:
            FollowUpResult:
                Generated follow-up sonucu.

                İçerdiği alanlar:
                    - follow_up_question
                    - reasoning
                    - confidence

        Raises:
            ValueError:
                - answer boşsa
                - Groq response boşsa
                - JSON parse başarısızsa
                - invalid FollowUpResult oluşursa

        Design Note:
            Bu method:
                orchestration layer

            gibi davranır.

            Gerçek follow-up reasoning:
                LLM prompt engineering

            içerisinde gerçekleşir.
        """

        logger.info(
            "follow_up_generation_started",
            question_id=question.id,
        )

        # ---------------------------------------------------------
        # ANSWER VALIDATION
        # ---------------------------------------------------------
        # Boş answer üzerinden meaningful follow-up üretilemez.
        #
        # strip():
        #   whitespace-only input'u da engeller.
        if not answer.strip():
            raise ValueError("Answer cannot be empty.")

        # ---------------------------------------------------------
        # PROMPT GENERATION
        # ---------------------------------------------------------
        # Candidate answer analizine uygun adaptive prompt oluşturulur.
        #
        # Prompt:
        #   - original question
        #   - expected points
        #   - candidate answer
        #
        # bilgilerini içerir.
        prompt = self._build_prompt(
            question=question,
            answer=answer,
        )

        # ---------------------------------------------------------
        # GROQ INFERENCE REQUEST
        # ---------------------------------------------------------
        # LLM'e follow-up generation isteği gönderilir.
        #
        # temperature=0.3:
        #   bir miktar creativity sağlar
        #   ancak hala kontrollü generation üretir.
        #
        # response_format=json_object:
        #   deterministic JSON output zorlar.
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        # ---------------------------------------------------------
        # RAW CONTENT EXTRACTION
        # ---------------------------------------------------------
        # Model text response'u alınır.
        content = response.choices[0].message.content

        # ---------------------------------------------------------
        # EMPTY RESPONSE VALIDATION
        # ---------------------------------------------------------
        # Provider bazen boş response dönebilir.
        #
        # Bu durumda parse işlemine geçilmez.
        if content is None or not content.strip():
            raise ValueError("Groq returned empty response.")

        # ---------------------------------------------------------
        # JSON PARSING + DOMAIN MAPPING
        # ---------------------------------------------------------
        # Model çıktısı parse edilerek typed domain model oluşturulur.
        #
        # Böylece:
        #   - type safety
        #   - validation
        #   - immutable result
        #
        # sağlanır.
        try:
            data = json.loads(content)

            logger.info(
                "follow_up_generated",
                confidence=data.get(
                    "confidence",
                    0.0,
                ),
            )

            return FollowUpResult(
                follow_up_question=data["follow_up_question"],
                reasoning=data.get("reasoning"),
                confidence=float(
                    data.get(
                        "confidence",
                        0.0,
                    )
                ),
            )

        except Exception as exc:
            raise ValueError(f"Failed to parse follow-up output: {exc}") from exc

    def _build_prompt(
        self,
        question: Question,
        answer: str,
    ) -> str:
        """
        Adaptive follow-up generation prompt'unu oluşturur.

        Bu prompt'un amacı:
            LLM'in:
                - candidate eksiklerini analiz etmesini
                - teknik derinliği ölçmesini
                - intelligent probing yapmasını

            sağlamaktır.

        Args:
            question:
                Original interview question.

            answer:
                Candidate answer.

        Returns:
            str:
                Groq LLM'e gönderilecek tam prompt.
        """

        # ---------------------------------------------------------
        # EXPECTED POINT FORMATTING
        # ---------------------------------------------------------
        # Expected point'ler bullet-list formatına çevrilir.
        #
        # Bu format:
        #   rubric readability
        #
        # açısından daha uygundur.
        expected_points = "\n".join(f"- {point}" for point in question.expected_points)

        # ---------------------------------------------------------
        # FOLLOW-UP GENERATION PROMPT
        # ---------------------------------------------------------
        # Prompt:
        #   - original question
        #   - expected concepts
        #   - candidate answer
        #
        # üzerinden adaptive probing ister.
        #
        # Amaç:
        #   shallow reasoning ve missing concepts'i açığa çıkarmaktır.
        return f"""
You are an adaptive AI interview system.

Your task:
Generate ONE intelligent follow-up question.

ORIGINAL QUESTION:
{question.text}

EXPECTED POINTS:
{expected_points}

CANDIDATE ANSWER:
{answer}

Analyze:
- missing concepts
- shallow reasoning
- missing technical depth
- vague explanations

Return ONLY valid JSON.

Schema:

{{
    "follow_up_question": "...",
    "reasoning": "...",
    "confidence": 0.0
}}
"""
