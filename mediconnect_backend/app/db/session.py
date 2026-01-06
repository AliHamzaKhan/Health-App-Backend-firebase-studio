from app.core.config import get_settings
from app.db_config import get_engine, get_session_local

settings = get_settings()

engine = get_engine(settings.DATABASE_URL)
SessionLocal = get_session_local(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
