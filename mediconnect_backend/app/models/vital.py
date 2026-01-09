from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Vital(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    value = Column(String)
    unit = Column(String, nullable=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    patient = relationship("Patient", back_populates="vitals")
