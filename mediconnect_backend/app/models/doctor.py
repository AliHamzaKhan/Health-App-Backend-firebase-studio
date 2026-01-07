from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    specialty = Column(String, index=True)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    photo_url = Column(String, name="photo")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")
    reviews = relationship("Review", back_populates="doctor")
    schedules = relationship("Schedule", back_populates="doctor")
