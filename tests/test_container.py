from src.container import Container


def test_container_builds_embedding_model() -> None:
    container = Container()

    model = container.build_embedding_model()

    assert model is not None


def test_container_builds_vector_store() -> None:
    container = Container()

    store = container.build_vector_store()

    assert store is not None


def test_container_builds_repository() -> None:
    container = Container()

    repository = container.build_question_repository()

    assert repository is not None


def test_container_builds_retrieval_service() -> None:
    container = Container()

    service = container.build_question_retrieval_service()

    assert service is not None
