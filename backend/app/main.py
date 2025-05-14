from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_jobs import router as job_router
from app.db.session import engine, Base
from app.models.job import Job
from app.models.backlink import Backlink
from app.api import routes_analytics
from app.tasks import backlink_task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backlink Tracker")
app.include_router(routes_analytics.router)

# 👇 CORS fix
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router, prefix="/jobs", tags=["Jobs"])
