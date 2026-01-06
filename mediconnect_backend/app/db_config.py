from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine(db_url: str):
    return create_engine(db_url, pool_pre_ping=True)

def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
