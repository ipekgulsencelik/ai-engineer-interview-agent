from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    LLM sağlayıcıları için ortak client interface'i.

    Bu sınıf doğrudan LLM çağrısı yapan somut bir client değildir.
    Bunun yerine Groq, OpenAI, Anthropic veya local model gibi farklı
    LLM provider'ları için ortak bir contract tanımlar.

    Amaç:
        Sistemin belirli bir LLM sağlayıcısına doğrudan bağımlı olmasını
        engellemektir.

    Bu interface sayesinde application/service katmanı sadece LLMClient
    abstraction'ını bilir. Hangi provider'ın kullanıldığı, hangi SDK'nın
    çağrıldığı veya API request'in nasıl atıldığı infrastructure katmanında
    saklanır.

    Desteklenebilecek provider örnekleri:
        - Groq
        - OpenAI
        - Anthropic
        - Ollama
        - Local HuggingFace model
        - MockLLMClient

    Neden interface kullanıyoruz?
        - Provider değiştirmek kolaylaşır.
        - Testlerde gerçek API çağrısı yapılmadan mock client kullanılabilir.
        - Dependency Inversion Principle uygulanır.
        - Service katmanı SDK detaylarından izole edilir.
        - API key, model adı, timeout, retry gibi detaylar burada tutulmaz.
        - Farklı provider'lar aynı generate contract'ı ile çalışabilir.

    Mimari konum:
        Bu interface application boundary üzerinde bir port gibi davranır.

        Application/service layer:
            Prompt oluşturur ve LLMClient.generate(...) çağırır.

        Interface:
            LLMClient

        Infrastructure layer:
            GroqLLMClient
            OpenAILLMClient
            AnthropicLLMClient
            LocalLLMClient
            MockLLMClient

    Önemli tasarım notu:
        Bu interface içerisinde provider-specific detaylar bulunmamalıdır.

        Yani burada:
            - API key
            - base URL
            - model name
            - SDK import'u
            - HTTP request logic
            - retry policy
            - rate limit handling

        yer almamalıdır.

        Bu detaylar somut client implementasyonlarına bırakılmalıdır.

    Kullanım örneği:
        service = SomeService(llm_client=GroqLLMClient(...))

        response = service.generate_feedback(...)

    Test kullanım örneği:
        service = SomeService(llm_client=MockLLMClient())

    Not:
        Şu an generate metodu string döndürmektedir.
        İlerleyen fazlarda token kullanımı, latency, model adı ve raw response
        gibi alanlar gerekiyorsa LLMResponse gibi typed bir response model'e
        geçmek daha doğru olacaktır.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> str:
        """
        LLM'den text response üretir.

        Bu method, bütün LLM provider implementasyonlarının uyması gereken
        ortak text generation contract'ıdır.

        Her somut client bu metodu kendi provider'ının SDK veya API yapısına
        göre implemente eder.

        Örnek:
            GroqLLMClient:
                Groq chat completion endpoint'ini çağırır.

            OpenAILLMClient:
                OpenAI responses/chat completion API'sini çağırır.

            AnthropicLLMClient:
                Anthropic messages API'sini çağırır.

            MockLLMClient:
                Test için sabit veya deterministic bir cevap döndürür.

        Args:
            prompt:
                LLM'e gönderilecek ana kullanıcı prompt'udur.

                Bu değer genellikle:
                    - değerlendirme prompt'u
                    - rubric prompt'u
                    - follow-up question üretme prompt'u
                    - feedback generation prompt'u

                olabilir.

                Boş olmamalıdır. Somut implementasyonlar boş prompt için
                ValueError fırlatabilir.

            system_prompt:
                Model davranışını yönlendiren opsiyonel sistem mesajıdır.

                Örnek kullanım:
                    - "You are a strict technical interviewer."
                    - "Return only valid JSON."
                    - "Evaluate the answer using the given rubric."

                None verilirse provider implementasyonu sadece user prompt ile
                generation yapabilir.

            temperature:
                Model çıktısının randomness / creativity seviyesini belirler.

                Düşük değerler:
                    - daha deterministic
                    - daha tutarlı
                    - evaluation işleri için daha güvenilir

                Yüksek değerler:
                    - daha yaratıcı
                    - daha çeşitli
                    - brainstorming veya alternatif üretim için daha uygun

                Bu projede default 0.2 seçilmiştir çünkü interview evaluation
                gibi scoring odaklı işlemlerde tutarlılık önemlidir.

            max_tokens:
                Modelin üretebileceği maksimum token sayısını sınırlar.

                None verilirse provider'ın default token limiti kullanılabilir.

                Kullanım amacı:
                    - maliyeti kontrol etmek
                    - çok uzun cevapları engellemek
                    - response süresini düşürmek
                    - JSON çıktının gereksiz uzamasını önlemek

        Returns:
            str:
                LLM tarafından üretilen ham text response.

                Örnek response:
                    "The candidate demonstrates a good understanding of RAG."

                JSON beklenen senaryolarda bile bu method string döndürür.
                JSON parse etme sorumluluğu bu interface'in değil,
                evaluator veya service katmanının sorumluluğudur.

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan LLMClient üzerinden
                çağrılamaz. Mutlaka somut bir subclass tarafından implemente
                edilmelidir.

            ValueError:
                Somut implementasyonlar boş prompt, geçersiz temperature veya
                geçersiz max_tokens durumlarında ValueError fırlatabilir.

            RuntimeError:
                Provider API hataları, timeout, rate limit veya bağlantı
                problemleri somut implementasyon tarafından RuntimeError gibi
                uygulama seviyesinde anlamlı hatalara dönüştürülebilir.

        Design Note:
            Bu interface'in görevi sadece text generation contract'ını
            tanımlamaktır.

            Prompt building, response parsing, scoring, retry policy veya
            provider-specific configuration bu interface'in sorumluluğu
            değildir.

            Böylece LLMClient küçük, temiz ve provider bağımsız kalır.
        """
        pass
