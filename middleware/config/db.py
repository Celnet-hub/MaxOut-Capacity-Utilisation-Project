from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .env import settings


db_engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()   # create DB session
    try:
        yield db          # pause, give `db` to the caller of the db session
    finally:
        db.close()        # resume here after the caller is finished