class SentenceTransformerEmbeddingProviderValidator:
    @staticmethod
    def validate_model_name(model_name: str | None) -> None:
        if model_name is None:
            return
        if not isinstance(model_name, str):
            raise TypeError("model_name must be a string")
        if not model_name.strip():
            raise ValueError("model_name cannot be empty")

    @staticmethod
    def validate_model(model: object) -> None:
        if model is None:
            raise ValueError("model cannot be None")
        if not hasattr(model, "encode"):
            raise TypeError("model must implement encode")

    @staticmethod
    def validate_text(text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        normalized = text.strip()
        if not normalized:
            raise ValueError("text cannot be empty")
        return normalized

    @staticmethod
    def validate_texts(texts: list[str]) -> list[str]:
        if not isinstance(texts, list):
            raise TypeError("texts must be a list")
        if not texts:
            raise ValueError("texts cannot be empty")
        return [SentenceTransformerEmbeddingProviderValidator.validate_text(t) for t in texts]