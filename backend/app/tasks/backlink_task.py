from app.core.celery_app import celery_app
from app.services.crawler import extract_backlinks
from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.models.backlink import Backlink

BATCH_SIZE = 100

def commit_backlinks_in_batches(db, backlinks, batch_size=BATCH_SIZE):
    for i in range(0, len(backlinks), batch_size):
        batch = backlinks[i:i+batch_size]
        try:
            db.bulk_save_objects(batch)
            db.commit()
        except Exception as e:
            print(f"❌ Error inserting batch {i//batch_size + 1}: {e}")
            db.rollback()

@celery_app.task(name="crawl_backlinks")
# def crawl_backlinks_task(job_id: int, url: str, target_domain: str):
#     db = SessionLocal()
#     job = db.query(Job).get(job_id)
#     if not job:
#         db.close()
#         return

#     job.status = JobStatus.in_progress
#     db.commit()

#     try:
#         results = extract_backlinks(url, target_domain)
#         backlinks = [
#             Backlink(job_id=job.id, **r) for r in results
#         ]
#         commit_backlinks_in_batches(db, backlinks)
#         job.status = JobStatus.completed
#     except Exception as e:
#         job.status = JobStatus.failed
#         print(f"❌ Job failed: {e}")
#     finally:
#         db.commit()
#         db.close()

def crawl_backlinks_task(job_id: int, url: str, target_domain: str):
    db = SessionLocal()
    print(f"🚀 Received crawl task for Job ID {job_id}")
    job = db.query(Job).get(job_id)
    
    if not job:
        print(f"❌ Job {job_id} not found in DB")
        db.close()
        return

    print(f"🔄 Setting Job {job_id} status to in_progress")
    job.status = JobStatus.in_progress
    db.commit()

    try:
        results = extract_backlinks(url, target_domain)
        backlinks = [
            Backlink(job_id=job.id, **r) for r in results
        ]
        commit_backlinks_in_batches(db, backlinks)
        job.status = JobStatus.completed
        print(f"✅ Job {job_id} completed successfully with {len(backlinks)} backlinks")
    except Exception as e:
        job.status = JobStatus.failed
        print(f"❌ Job {job_id} failed: {e}")
    finally:
        db.commit()
        db.close()
