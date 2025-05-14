==============================
🔗 BACKLINK TRACKER - README
==============================

This is a full-featured backlink tracking system built with:

- FastAPI (backend APIs)
- PostgreSQL (database)
- Celery + Redis (asynchronous task processing)
- React + Vite (frontend)
- Docker Compose (for easy launch)

------------------------------------------
🔧 REQUIREMENTS (For Local Dev)
------------------------------------------

- Python 3.10+
- Node.js 16+
- PostgreSQL 13+
- Redis
- Docker & Docker Compose (for containerized launch)

------------------------------------------
📦 PROJECT STRUCTURE
------------------------------------------

app/
├── api/
│   ├── routes_jobs.py
│   └── routes_analytics.py
├── core/
│   └── celery_app.py
├── db/
│   └── session.py
├── models/
│   └── job.py
├── schemas/
│   └── job.py
├── tasks/
│   ├── backlink_task.py
│   └── scheduler.py
├── logger.py
frontend/
├── src/
│   ├── components/
│   ├── App.jsx
│   ├── api.js
│   └── main.jsx
docker-compose.yml
README.txt

------------------------------------------
🚀 RUN LOCALLY (Without Docker)
------------------------------------------

1. Create `.env` file in root (backend):

    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/backlink_db
    CELERY_BROKER_URL=redis://localhost:6379/0

2. Install dependencies:

    pip install -r requirements.txt
    npm install --prefix frontend

3. Start backend:

    uvicorn app.main:app --reload

4. Start Celery and Beat:

    celery -A app.core.celery_app.celery_app worker --loglevel=info
    celery -A app.core.celery_app.celery_app beat --loglevel=info

5. Start frontend:

    cd frontend
    npm run dev

------------------------------------------
🐳 RUN WITH DOCKER COMPOSE
------------------------------------------

1. Create `.env` file in the same folder as `docker-compose.yml`:

    POSTGRES_DB=backlink_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    REDIS_URL=redis://redis:6379/0

2. Launch containers:

    docker-compose up --build

3. Access services:

    - Backend: http://localhost:8000/docs
    - Frontend: http://localhost:5173/

------------------------------------------
📤 API TEST EXAMPLE (POST /jobs/)
------------------------------------------

Payload:

{
  "urls": ["https://example.com"],
  "target_domains": ["example.com"],
  "rate_limit": 2,
  "schedule": null,
  "run_at": null
}

------------------------------------------
📉 ROLLBACK COLUMNS FROM DATABASE
------------------------------------------

To remove added columns manually (rate_limit, schedule, run_at):

```sql
ALTER TABLE jobs DROP COLUMN IF EXISTS rate_limit;
ALTER TABLE jobs DROP COLUMN IF EXISTS schedule;
ALTER TABLE jobs DROP COLUMN IF EXISTS run_at;
```

------------------------------------------
📝 TIPS & TROUBLESHOOTING
------------------------------------------

- Use `print(job.model_dump())` in routes for payload debug.
- If you see 422 errors, ensure:
  - Correct route: POST /jobs/
  - Payload matches schema exactly.
- Ensure Redis is running before starting Celery.
- PostgreSQL container must persist DB volume or use bind mount.

------------------------------------------
❤️ BUILT WITH
------------------------------------------

- FastAPI: https://fastapi.tiangolo.com/
- Celery: https://docs.celeryq.dev
- React + Vite: https://vitejs.dev
- PostgreSQL: https://www.postgresql.org
- Docker: https://docs.docker.com