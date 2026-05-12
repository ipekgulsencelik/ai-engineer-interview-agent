from __future__ import annotations

from src.domain.config.provider_config import ProviderConfig
from src.application.ports.llm_client import LLMClient
from src.domain.llm.llm_response import LLMResponse


class MockLLMClient(LLMClient):
    """
    Test ve local development için kullanılan sahte LLM client.

    Bu sınıf gerçek bir LLM provider'a bağlanmaz.
    Yani:
        - Groq API
        - OpenAI API
        - Anthropic API
        - Ollama server
        - local inference engine
    gibi external sistemlerle iletişim kurmaz.

    Amaç:
        LLM bağımlılığı olan servislerin gerçek API çağrısı yapılmadan
        test edilebilmesini sağlamaktır.

    Bu client özellikle şu durumlarda kullanılır:
        - unit test yazarken
        - local development sırasında
        - internet bağlantısı olmadan geliştirme yaparken
        - API key olmadan sistemi çalıştırırken
        - CI/CD pipeline testlerinde
        - deterministic output gereken senaryolarda
        - hızlı demo akışlarında

    Neden MockLLMClient gerekli?
        Gerçek LLM provider kullanıldığında:
            - API maliyeti oluşur
            - response süresi uzayabilir
            - network bağımlılığı oluşur
            - rate limit problemleri yaşanabilir
            - nondeterministic output üretilebilir
            - testler flaky hale gelebilir

        MockLLMClient bu problemlerin tamamını ortadan kaldırır.

    Bu sayede:
        - Service layer güvenli şekilde test edilir.
        - Prompt pipeline doğrulanabilir.
        - Evaluation flow çalıştırılabilir.
        - LLM entegrasyonu olmadan sistem ayağa kaldırılabilir.
        - CLI/UI hızlı şekilde demo yapılabilir.

    Mimari konum:
        Interface:
            LLMClient

        Concrete test implementation:
            MockLLMClient

        Kullanıldığı yerler:
            - Evaluator testleri
            - Prompt service testleri
            - Interview pipeline integration testleri
            - Local CLI demo akışı

    Tasarım notu:
        MockLLMClient gerçek provider davranışını birebir taklit etmeye
        çalışmaz.

        Bunun yerine:
            - stabil
            - hızlı
            - deterministic
            - predictable
        davranış sunmayı hedefler.

    Deterministic output neden önemli?
        Çünkü testlerde aynı input için her zaman aynı output alınmalıdır.

        Bu sayede:
            - assertion yazmak kolaylaşır
            - flaky testler azalır
            - CI pipeline daha güvenilir çalışır

    Önemli:
        Bu sınıf production kullanım için tasarlanmamıştır.

        Gerçek semantic generation, reasoning veya evaluation yeteneği yoktur.

    İleride eklenebilecek gelişmiş mock varyasyonları:
        - ConfigurableMockLLMClient
        - DelayedMockLLMClient
        - ErrorSimulationMockLLMClient
        - ScenarioBasedMockLLMClient
        - StreamingMockLLMClient

    Örnek kullanım:
        llm_client = MockLLMClient()

        response = llm_client.generate(
            prompt="Explain how RAG works."
        )

        print(response)

    Beklenen çıktı:
        "Mock LLM response."
    """

    DEFAULT_RESPONSE_TEXT = "This is a mock response."
    MODEL_NAME = "mock-llm"


    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        stop: list[str] | None = None,
    ) -> LLMResponse:
        """
        Deterministic mock text response üretir.

        Bu method gerçek bir LLM inference işlemi yapmaz.
        Bunun yerine sabit ve tahmin edilebilir bir string döndürür.

        Args:
            prompt:
                LLM'e gönderilecek ana kullanıcı prompt'udur.

                Boş olmamalıdır.

                Gerçek provider implementasyonlarında bu değer:
                    - chat completion
                    - prompt template
                    - evaluation request
                    - summarization request
                    - question generation
                gibi işlemler için kullanılabilir.

            system_prompt:
                Model davranışını yönlendiren opsiyonel sistem prompt'udur.

                Mock implementation içerisinde aktif kullanılmaz.
                Ancak interface contract'ına uyum sağlamak için parametre
                korunur.

                Gerçek örnek:
                    "You are a strict technical interviewer."

            temperature:
                Generation randomness seviyesini temsil eder.

                Mock implementation deterministic çalıştığı için bu parametre
                sonucu değiştirmez.

                Ancak gerçek provider implementasyonlarıyla aynı method
                signature'ını korumak için burada bulunur.

            max_tokens:
                Maksimum output token limiti.

                Mock implementation içinde aktif kullanılmaz.

                Ancak gerçek provider implementasyonlarıyla contract uyumu
                için parametre korunur.

            stop:
                Generation'ı durduracak token veya string listesi.

                Mock implementation içinde aktif kullanılmaz.
                
                Ancak gerçek provider implementasyonlarıyla uyum için parametre
                korunur.

        Returns:
            LLMResponse:
                Sabit mock response döndürür.

                Varsayılan çıktı:
                    "This is a mock response."

                Bu response:
                    - deterministic
                    - hızlı
                    - test dostu
                olacak şekilde bilinçli olarak sabit tutulmuştur.

        Raises:
            ValueError:
                prompt boş veya yalnızca whitespace karakterlerinden oluşuyorsa
                fırlatılır.

        Design Note:
            Bu methodun amacı semantic kalite üretmek değil,
            LLM bağımlı sistemlerin çalıştığını doğrulamaktır.

            Örneğin:
                - service orchestration
                - dependency injection
                - pipeline akışı
                - exception handling
                - response parsing
            gibi sistem davranışları bu mock client ile güvenli şekilde
            test edilebilir.

        Example:
            client = MockLLMClient()

            result = client.generate(
                prompt="Explain vector databases."
            )

            print(result)

        Output:
            "This is a mock response."
        """

        # ---------------------------------------------------------
        # PROMPT VALIDATION
        # ---------------------------------------------------------
        # Boş prompt anlamlı bir generation isteği değildir.
        #
        # strip() kullanmamızın nedeni:
        #   "   " gibi sadece whitespace içeren string'leri de
        #   geçersiz kabul etmektir.
        #
        # Gerçek provider implementasyonlarında da benzer validation
        # yapılması beklenir.
        self._validate_prompt(prompt)

        # ---------------------------------------------------------
        # PARAMETRE KULLANIMI
        # ---------------------------------------------------------
        # Mock implementation içinde bu parametreler aktif kullanılmaz.
        # Ancak gerçek provider implementasyonlarıyla aynı method
        # signature'ını korumak için burada bulunur.
        _ = system_prompt, temperature, max_tokens, stop

        # ---------------------------------------------------------
        # DETERMINISTIC MOCK RESPONSE
        # ---------------------------------------------------------
        # Sabit response döndürülür.
        #
        # Neden sabit?
        #   - predictable test output sağlamak için
        #   - flaky testleri önlemek için
        #   - hızlı local development için
        #   - gerçek API maliyetinden kaçınmak için
        #
        # Bu response gerçek semantic generation temsil etmez.
        return LLMResponse(
            text=self.DEFAULT_RESPONSE_TEXT,
            model_name=self.MODEL_NAME,
            tokens_used=0,
            latency_seconds=0.0,
            raw_output=None,
        )


    @staticmethod
    def _validate_prompt(
        prompt: str,
    ) -> None:
        """
        Prompt input'unu doğrular.
        
        Bu method, generate(...) metoduna gelen prompt parametresinin
        geçerli bir string olduğunu doğrular.

        Validation kuralları:
            - prompt bir string olmalıdır
            - prompt boş veya sadece whitespace karakterlerinden oluşmamalıdır

        Raises:
            ValueError:
                prompt boş veya sadece whitespace karakterlerinden oluşuyorsa
                fırlatılır.

            TypeError:
                prompt bir string değilse fırlatılır.
        """

        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string.")

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
