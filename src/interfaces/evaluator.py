from abc import ABC, abstractmethod

from src.domain.question.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class Evaluator(ABC):
    """
    Aday cevabını değerlendiren evaluator interface'i.

    Bu sınıf doğrudan çalışan bir evaluator değildir.
    Bunun yerine sistemde kullanılacak tüm evaluator implementasyonları
    için ortak bir contract / interface tanımlar.

    Amaç:
        Interview sistemi içerisinde aday cevaplarını değerlendirme
        sorumluluğunu soyutlamaktır.

    Bu abstraction sayesinde sistem farklı değerlendirme stratejilerini
    aynı servis katmanı üzerinden kullanabilir.

    Örnek evaluator implementasyonları:
        - MockEvaluator:
            Test ve development ortamlarında deterministic sonuç üretir.

        - GroqEvaluator:
            Groq üzerinden çalışan LLM tabanlı değerlendirme yapar.

        - OpenAIEvaluator:
            OpenAI modellerini kullanarak rubric-based değerlendirme yapar.

        - RuleBasedEvaluator:
            Anahtar kelime, beklenen kavramlar veya basit skor kuralları
            üzerinden deterministic değerlendirme yapar.

    Neden interface kullanıyoruz?
        - AnswerEvaluationService somut bir evaluator'a bağımlı olmaz.
        - Dependency Inversion Principle uygulanır.
        - Test yazmak kolaylaşır.
        - Gerçek LLM provider'ı değiştirmek servis katmanını etkilemez.
        - Mock evaluator ile hızlı ve maliyetsiz test yapılabilir.
        - İleride ensemble evaluator veya hybrid evaluator eklenebilir.

    Mimari konum:
        Domain/Application boundary üzerinde yer alan bir port gibi düşünülebilir.

        Service layer:
            AnswerEvaluationService

        Interface:
            Evaluator

        Infrastructure implementations:
            MockEvaluator
            GroqEvaluator
            OpenAIEvaluator
            RuleBasedEvaluator

    Önemli tasarım notu:
        Bu interface herhangi bir provider bilgisi içermez.
        Yani burada:
            - API key
            - model name
            - temperature
            - HTTP client
            - Groq/OpenAI SDK detayları

        bulunmamalıdır.

        Bu detaylar infrastructure katmanındaki somut evaluator
        class'larında yönetilmelidir.

    Beklenen çıktı:
        evaluate metodu provider bağımsız standart bir dict döndürür.

        Örnek:
            {
                "score": 8,
                "feedback": "Answer is technically correct but lacks depth.",
                "missing_keywords": ["embedding", "retrieval"],
                "follow_up_question": "How would you improve retrieval quality?"
            }

    Not:
        Şu an dönüş tipi dict olarak bırakılmıştır.
        Faz ilerledikçe EvaluationResult gibi typed bir domain model'e
        dönüştürülmesi daha güvenli ve sürdürülebilir olacaktır.
    """

    @abstractmethod
    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        """
        Adayın verdiği cevabı değerlendirir.

        Bu method, bütün evaluator implementasyonlarının uyması gereken
        ortak değerlendirme contract'ıdır.

        Her somut evaluator bu metodu kendi stratejisine göre implemente eder.

        Örnek:
            MockEvaluator:
                Sabit veya deterministic skor döndürür.

            GroqEvaluator:
                Question ve answer bilgisinden prompt oluşturur,
                LLM'e gönderir ve JSON evaluation sonucu döndürür.

            RuleBasedEvaluator:
                Cevap içerisinde beklenen keyword'leri arar,
                coverage oranına göre skor hesaplar.

        Args:
            question:
                Adaya sorulan Question domain modeli.

                Bu model genellikle şu bilgileri içerir:
                    - question id
                    - question text
                    - category
                    - level
                    - difficulty
                    - expected points
                    - keywords
                    - question type

                Evaluator, bu bilgileri kullanarak cevabı bağlamlı şekilde
                değerlendirebilir.

            answer:
                Adayın soruya verdiği ham metin cevaptır.

                Bu değer:
                    - boş olmamalıdır
                    - strip edilmiş şekilde kontrol edilebilir
                    - evaluator implementasyonu içerisinde validate edilebilir

                Boş cevap durumunda implementasyon tercihine göre:
                    - ValueError fırlatılabilir
                    - score=0 döndürülebilir
                    - özel bir feedback mesajı üretilebilir

        Returns:
            EvaluationResult:
                Provider bağımsız evaluation sonucu.

                Tavsiye edilen minimum alanlar:
                    {
                        "score": int | float,
                        "feedback": str,
                        "missing_keywords": list[str],
                    }

                Opsiyonel alanlar:
                    {
                        "technical_accuracy": int | float,
                        "depth": int | float,
                        "communication": int | float,
                        "follow_up_question": str,
                        "raw": dict | str,
                    }

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan Evaluator üzerinden
                çağrılamaz. Mutlaka somut bir subclass tarafından implemente
                edilmelidir.

            ValueError:
                Somut implementasyonlar boş cevap veya geçersiz question
                durumlarında ValueError fırlatabilir.

        Design Note:
            Bu interface'in amacı evaluation davranışını standartlaştırmaktır.
            Skorlama algoritması, prompt yapısı, LLM provider detayı veya
            parsing logic burada bulunmamalıdır.

            Bu sayede interface temiz kalır, implementation detayları ise
            infrastructure katmanında izole edilir.
        """
        pass
