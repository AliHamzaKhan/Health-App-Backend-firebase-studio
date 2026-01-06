import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, initialize_database
from app.core.config import get_settings
from app.db.session import get_db
from app.db.base import Base

engine = create_engine(get_settings().DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    initialize_database()
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
