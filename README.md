# AI Engineer Interview Agent

AI Engineer Interview Agent, adayların teknik mülakat sürecini desteklemek için tasarlanmış bir backend + UI projesidir.

## Quickstart

### 1) Gereksinimler
- Python **3.11+**
- `uv` (önerilen) veya `pip`

### 2) Kurulum
```bash
uv sync
```

Alternatif:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3) Environment ayarları
Kök dizinde `.env` dosyası oluşturun:

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

> Not: Gerçek production ortamında secret'ları `.env` yerine secret manager ile yönetin.

---

## Uygulamayı Çalıştırma

### API (FastAPI)
```bash
uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

Swagger:
- http://localhost:8000/docs
- http://localhost:8000/redoc

### UI (Streamlit)
```bash
uv run streamlit run src/ui/app.py
```

---

## Temel API Endpointleri

Base prefix: `/api/v1`

### 1) Health
`GET /api/v1/health`

Örnek:
```bash
curl -X GET http://localhost:8000/api/v1/health
```

### 2) Evaluation
`POST /api/v1/evaluations`

Örnek:
```bash
curl -X POST http://localhost:8000/api/v1/evaluations \
  -H "Content-Type: application/json" \
  -d '{
    "question": {
      "id": "q-1",
      "text": "Explain CAP theorem.",
      "category": "system_design",
      "level": "mid",
      "question_type": "technical",
      "difficulty": "medium",
      "skills": ["distributed_systems"],
      "source": "manual"
    },
    "answer": "CAP theorem says consistency, availability, partition tolerance..."
  }'
```

### 3) Retrieval (Next Question)
`POST /api/v1/retrieval/next-question`

Örnek:
```bash
curl -X POST http://localhost:8000/api/v1/retrieval/next-question \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python backend concurrency",
    "current_level": "junior",
    "top_k": 10
  }'
```

### 4) Interview Step
`POST /api/v1/interview/step`

Örnek:
```bash
curl -X POST http://localhost:8000/api/v1/interview/step \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data modeling",
    "current_level": "mid",
    "answer": "I would design ..."
  }'
```

### 5) CV Analysis
`POST /api/v1/cv/analyze` (multipart form-data)

Örnek:
```bash
curl -X POST http://localhost:8000/api/v1/cv/analyze \
  -F "file=@/absolute/path/to/cv.pdf"
```

---

## Test ve Kalite Komutları

### Tüm testler
```bash
PYTHONPATH=. pytest -q
```

### Belirli bir test dosyası
```bash
PYTHONPATH=. pytest -q tests/domain/normalizers/test_question_category_normalizer.py
```

### Lint (ruff)
```bash
uv run ruff check .
```

### Format kontrolü (ruff)
```bash
uv run ruff format --check .
```

### Type check (pyright)
```bash
uv run pyright
```

---

## Proje Yapısı (Özet)

- `src/api`: FastAPI route, schema, mapper, dependency
- `src/application`: use-case/service orchestration
- `src/domain`: core domain model, policy, validator
- `src/infrastructure`: provider/adapter/container/repository
- `src/ui`: Streamlit UI
- `tests`: test suite

---

## Faydalı Geliştirme Notları

- Projede `pytest` için `pythonpath = ["."]` ayarı bulunuyor.
- API için önerilen giriş noktası `src.api.app:app`.
- Ortam değişkenlerini düzenlerken `src/config/settings.py` ile uyumlu değerler verin.
