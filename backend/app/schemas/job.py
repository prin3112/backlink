from pydantic import BaseModel
from typing import Optional
from datetime import time

class JobCreate(BaseModel):
    url: str
    target_domain: str
    schedule: Optional[str] = None  # "daily", "weekly", "monthly", or None
    run_at: Optional[time] = None   # format: "HH:MM"

class JobResponse(JobCreate):
    id: int
    status: str

    class Config:
        orm_mode = True
