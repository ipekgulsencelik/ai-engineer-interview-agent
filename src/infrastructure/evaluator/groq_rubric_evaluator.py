import json

from groq import Groq

from src.config.settings import settings
from src.domain.question.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)
from src.interfaces.evaluator import Evaluator
from src.logging.logger import logger


class GroqRubricEvaluator(Evaluator):
    """
    Groq tabanlı gerçek LLM evaluator implementation'ı.

    Bu class'ın amacı:
        Candidate answer'ı Groq üzerindeki bir LLM modeline göndererek
        rubric-based evaluation sonucu üretmektir.

    Bu evaluator:
        - gerçek LLM çağrısı yapar
        - aday cevabını değerlendirir
        - model çıktısını JSON olarak parse eder
        - sonucu EvaluationResult domain modeline dönüştürür

    Mimari konum:
        Interface:
            Evaluator

        Concrete implementation:
            GroqRubricEvaluator

        Kullanıldığı yer:
            AnswerEvaluationService

    Neden Evaluator interface'ini implemente ediyor?
        Çünkü application/service katmanı Groq'u doğrudan bilmemelidir.

        AnswerEvaluationService yalnızca Evaluator abstraction'ına bağımlı
        kalmalıdır.

        Böylece:
            - MockEvaluator
            - GroqRubricEvaluator
            - OpenAIRubricEvaluator
            - RuleBasedEvaluator

        aynı contract üzerinden kullanılabilir.

    Bu class ne yapar?
        ✔ Groq client oluşturur
        ✔ rubric prompt üretir
        ✔ LLM'e evaluation isteği gönderir
        ✔ JSON response parse eder
        ✔ EvaluationResult döndürür

    Bu class ne yapmaz?
        ✘ question seçmez
        ✘ level transition yapmaz
        ✘ interview orchestration yapmaz
        ✘ skor geçmişi tutmaz
        ✘ repository'den veri çekmez

    Önemli:
        Bu class infrastructure implementation'dır.
        Çünkü dış bir provider olan Groq SDK'sına bağımlıdır.
    """

    def __init__(self) -> None:
        """
        GroqRubricEvaluator instance'ı oluşturur.

        Bu aşamada:
            - GROQ_API_KEY kontrol edilir
            - Groq client initialize edilir
            - kullanılacak model adı settings üzerinden alınır

        Raises:
            ValueError:
                GROQ_API_KEY tanımlı değilse fırlatılır.
        """

        # ---------------------------------------------------------
        # API KEY VALIDATION
        # ---------------------------------------------------------
        # Gerçek Groq API çağrısı yapılacağı için API key zorunludur.
        #
        # Eğer API key yoksa evaluator çalışamaz.
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing.")

        # ---------------------------------------------------------
        # GROQ CLIENT INITIALIZATION
        # ---------------------------------------------------------
        # Groq SDK client'ı oluşturulur.
        #
        # Bu client LLM chat completion çağrıları için kullanılacaktır.
        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        # ---------------------------------------------------------
        # MODEL CONFIGURATION
        # ---------------------------------------------------------
        # Model adı merkezi settings üzerinden alınır.
        #
        # Böylece model değiştirmek için kod değiştirmek gerekmez.
        self.model = settings.GROQ_MODEL_NAME

    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        """
        Candidate answer'ı rubric-based şekilde değerlendirir.

        Bu method Evaluator interface contract'ına uyar.

        Akış:
            1. Answer validation yapılır.
            2. Question içinden gerekli bilgiler alınır.
            3. Rubric prompt oluşturulur.
            4. Groq LLM çağrısı yapılır.
            5. Model çıktısı JSON olarak parse edilir.
            6. EvaluationResult domain modeli döndürülür.

        Args:
            question:
                Adaya sorulan Question domain modeli.

                Kullanılan alanlar:
                    - question.text
                    - question.expected_points
                    - question.keywords

            answer:
                Adayın verdiği ham text cevaptır.

        Returns:
            EvaluationResult:
                Typed evaluation sonucu.

        Raises:
            ValueError:
                Answer boşsa veya LLM çıktısı parse edilemezse fırlatılır.
        """

        logger.info(
            "evaluation_started",
            question=question.text,
        )

        # ---------------------------------------------------------
        # ANSWER VALIDATION
        # ---------------------------------------------------------
        # Boş cevap evaluation için anlamlı değildir.
        if not answer.strip():
            raise ValueError("Answer cannot be empty.")

        # ---------------------------------------------------------
        # PROMPT BUILDING
        # ---------------------------------------------------------
        # Rubric prompt ayrı helper method ile oluşturulur.
        #
        # Böylece evaluate method'u orchestration seviyesinde temiz kalır.
        prompt = self._build_prompt(
            question=question.text,
            answer=answer,
            expected_points=question.expected_points,
        )

        # ---------------------------------------------------------
        # GROQ LLM REQUEST
        # ---------------------------------------------------------
        # Candidate answer LLM'e gönderilir.
        #
        # temperature=0.2:
        #   Evaluation task'lerinde daha deterministic sonuç almak için
        #   düşük tutulur.
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        # ---------------------------------------------------------
        # RAW CONTENT EXTRACTION
        # ---------------------------------------------------------
        # Groq response içerisinden model text çıktısı alınır.
        content = response.choices[0].message.content

        if content is None or not content.strip():
            raise ValueError("Groq returned empty response.")

        # ---------------------------------------------------------
        # JSON PARSING + DOMAIN MAPPING
        # ---------------------------------------------------------
        # Modelden yalnızca valid JSON dönmesi beklenir.
        #
        # Parse edilen data, EvaluationResult domain modeline çevrilir.
        try:
            data = json.loads(content)

            logger.info(
                "evaluation_completed",
                score=data["score"],
                technical_accuracy=data.get(
                    "technical_accuracy",
                    0,
                ),
                depth=data.get(
                    "depth",
                    0,
                ),
            )

            return EvaluationResult(
                score=float(data["score"]),
                feedback=data["feedback"],
                technical_accuracy=float(
                    data.get(
                        "technical_accuracy",
                        0,
                    )
                ),
                depth=float(
                    data.get(
                        "depth",
                        0,
                    )
                ),
                communication=float(
                    data.get(
                        "communication",
                        0,
                    )
                ),
                missing_keywords=data.get(
                    "missing_keywords",
                    [],
                ),
                follow_up_question=data.get("follow_up_question"),
            )

        except Exception as exc:
            raise ValueError(f"Failed to parse evaluator output: {exc}") from exc

    def _build_prompt(
        self,
        question: str,
        answer: str,
        expected_points: list[str],
    ) -> str:
        """
        LLM evaluation rubric prompt'unu oluşturur.

        Bu methodun amacı:
            LLM'e net, kontrollü ve JSON-only response üretecek şekilde
            yapılandırılmış evaluation instruction vermektir.

        Args:
            question:
                Adaya sorulan soru metni.

            answer:
                Adayın verdiği cevap.

            expected_points:
                Cevapta beklenen temel teknik noktalar.

        Returns:
            str:
                Groq LLM'e gönderilecek tam prompt.
        """

        # ---------------------------------------------------------
        # EXPECTED POINTS FORMAT
        # ---------------------------------------------------------
        # Expected point listesi bullet formatına çevrilir.
        #
        # Bu format LLM'in rubric'i daha kolay takip etmesini sağlar.
        expected = "\n".join(f"- {point}" for point in expected_points)

        # ---------------------------------------------------------
        # RUBRIC PROMPT
        # ---------------------------------------------------------
        # Modelden yalnızca JSON dönmesi istenir.
        #
        # Bu çok önemlidir çünkü evaluate method'u json.loads(content)
        # ile parse işlemi yapmaktadır.
        return f"""
You are a strict AI interview evaluator.

Evaluate the candidate answer based on the question and expected points.

QUESTION:
{question}

EXPECTED POINTS:
{expected}

CANDIDATE ANSWER:
{answer}

Return ONLY valid JSON.

Required schema:

{{
    "score": 0-10,
    "feedback": "...",
    "technical_accuracy": 0-10,
    "depth": 0-10,
    "communication": 0-10,
    "missing_keywords": [],
    "follow_up_question": "..."
}}
"""
