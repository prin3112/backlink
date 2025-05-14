from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base

class Backlink(Base):
    __tablename__ = "backlinks"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    source_url = Column(String)
    target_url = Column(String)
    rel = Column(String)
    title = Column(String)