from sqlalchemy import Column, Integer, String, Enum, DateTime, Time, func
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class JobStatus(str, enum.Enum):
    queued = "queued"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    target_domain = Column(String, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.queued)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    schedule = Column(String, nullable=True)
    run_at = Column(Time, nullable=True)