


from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Symptom(Base):
    __tablename__ = "symptoms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
