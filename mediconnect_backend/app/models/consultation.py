from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Consultation(Base):
    __tablename__ = "consultation_details"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointment.id"))
    hpi = Column(Text, nullable=True)
    soap_note = Column(Text, nullable=True)
    icd_codes = Column(String, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    referral = Column(String, nullable=True)
    
    appointment = relationship("Appointment", back_populates="consultation_details")