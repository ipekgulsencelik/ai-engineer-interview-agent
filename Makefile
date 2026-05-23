run-api:
	uv run uvicorn src.api.app:app --reload

run-ui:
	uv run streamlit run src/ui/app.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix

typecheck:
	uv run pyright

docker-build:
	docker build -t ai-interview-agent .

docker-up:
	docker compose up --build

index-questions:
	uv run python src/scripts/index_question_bank.py