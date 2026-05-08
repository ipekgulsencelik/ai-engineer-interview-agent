from src.config.settings import settings


def test_settings_load_successfully() -> None:
    assert settings.APP_NAME == "AI Engineer Interview Agent"

    assert settings.EMBEDDING_MODEL_NAME == "all-MiniLM-L6-v2"

    assert settings.CHROMA_COLLECTION_NAME == "questions"
