from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.backlink import Backlink

router = APIRouter()

@router.get("/analytics/{job_id}")
def get_analytics(job_id: int, db: Session = Depends(get_db)):
    backlinks = db.query(Backlink).filter(Backlink.job_id == job_id).all()
    return [
        {
            "source_url": b.source_url,
            "target_url": b.target_url,
            "rel": b.rel,
            "title": b.title
        }
        for b in backlinks
    ]
