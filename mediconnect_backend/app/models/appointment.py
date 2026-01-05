from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    date = Column(Date)
    time = Column(Time)
    reason = Column(String)
    status = Column(String, default="UPCOMING") # UPCOMING, COMPLETED, CANCELLED
    notes = Column(String, nullable=True)
    review_given = Column(Integer, default=0)
    reminder_sent = Column(Boolean, default=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    consultation_details = relationship("Consultation", uselist=False, back_populates="appointment", cascade="all, delete-orphan")
    review = relationship("Review", uselist=False, back_populates="appointment", cascade="all, delete-orphan")
