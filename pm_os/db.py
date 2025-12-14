from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pm_os.config import settings
from pm_os.models import Base

engine = create_engine(f"sqlite:///{settings.db_path}", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

