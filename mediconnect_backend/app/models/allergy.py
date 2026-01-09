from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Allergy(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
