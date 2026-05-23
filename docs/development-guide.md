# Development Guide

## Architecture Overview

Project layers:
- `src/api`: FastAPI routes, schemas, mappers, dependencies
- `src/application`: orchestration services and use-cases
- `src/domain`: business rules, validators, policies, entities/value objects
- `src/infrastructure`: adapters, containers, integrations (LLM/vector store)
- `src/ui`: Streamlit UI
- `tests`: unit/integration tests

## Quickstart

### Requirements
- Python 3.11+
- `uv`

### Install
```bash
uv sync
```

### Environment
Create `.env` in repository root (sample values):
```env
APP_NAME=AI Engineer Interview Agent
ENV=development
QUESTION_DATA_PATH=data/questions.json
CHROMA_PERSIST_DIR=data/chroma
CHROMA_COLLECTION_NAME=questions
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

## Running Locally

### API
```bash
uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

### UI
```bash
uv run streamlit run src/ui/app.py
```

## Quality Gates

Run before opening a PR:
```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

CI enforces the same checks in `.github/workflows/ci.yml`.

## Dependency Inversion Principle (DIP)

`ServiceContainer` is wired to accept an injectable LLM client factory:
- constructor arg: `llm_client_factory: Callable[[], LLMClient] | None`
- default factory: `GroqLLMClient`

This allows swapping concrete implementations without changing orchestration code.

## Testing Guidelines

- Prefer **behavioral tests** with fakes/mocks over source-string assertions.
- Keep tests focused on orchestration outcomes and contract expectations.
- For scoring/validation, use domain-valid fixtures (e.g., `difficulty` must match current constraints).

## Package/Import Guidelines

- Keep `__init__.py` in import-critical folders (already present in key domain packages).
- Add compatibility aliases only when migration/backward-compatibility is necessary.

## PR Checklist

- [ ] `uv run ruff check .`
- [ ] `uv run pyright`
- [ ] `uv run pytest -q`
- [ ] Update docs if behavior/config changed
- [ ] Keep dependency direction clean (domain/application should not depend on infrastructure concretes)
