from app.db.session import engine
from app.models.job import Base

Base.metadata.create_all(bind=engine)
