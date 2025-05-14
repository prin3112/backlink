
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.schemas.job import JobCreate
# from app.db.session import SessionLocal
# from app.models.job import Job, JobStatus
# from app.tasks.backlink_task import crawl_backlinks_task

# router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/")
# def create_job(job: JobCreate, db: Session = Depends(get_db)):
#     new_job = Job(url=job.url, target_domain=job.target_domain, status=JobStatus.queued)
#     db.add(new_job)
#     db.commit()
#     db.refresh(new_job)
#     crawl_backlinks_task.delay(new_job.id, job.url, job.target_domain)
#     return {"job_id": new_job.id, "status": new_job.status}

# @router.get("/")
# def list_jobs(db: Session = Depends(get_db)):
#     jobs = db.query(Job).order_by(Job.created_at.desc()).all()
#     return jobs

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.job import JobCreate
from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.tasks.backlink_task import crawl_backlinks_task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ POST / — create a job, but run it only if not scheduled
@router.post("/")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(
        url=job.url,
        target_domain=job.target_domain,
        status=JobStatus.queued,
        schedule=job.schedule,
        run_at=job.run_at,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    if not job.schedule or job.schedule == "once":
        crawl_backlinks_task.delay(new_job.id, job.url, job.target_domain)

    return {"job_id": new_job.id, "status": new_job.status}

# ✅ GET / — list all jobs
@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return jobs
