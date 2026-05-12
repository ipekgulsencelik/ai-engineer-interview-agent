from __future__ import annotations

from abc import ABC, abstractmethod

from src.application.models.llm_request import LLMRequest
from src.application.models.llm_response import LLMResponse


class LLMClient(ABC):
    """
    Text generation provider'ları için application port.

    Bu port application katmanını OpenAI, Groq, Anthropic veya local model
    gibi concrete provider implementasyonlarından izole eder.

    Implementasyonlar infrastructure katmanında yer almalıdır.
    """

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Provider-independent LLMRequest üzerinden text generation sonucu üretir.

        Args:
            request:
                Provider-independent text generation request modeli.

        Returns:
            LLMResponse:
                Normalize edilmiş provider-independent generation sonucu.
        """
        ...