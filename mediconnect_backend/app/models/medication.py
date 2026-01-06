from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class Medication(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    price = Column(Float, nullable=False)
