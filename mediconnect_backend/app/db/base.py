from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Float,
    Date
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base, relationship, backref
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # PATIENT, DOCTOR, ADMIN
    profile_pic = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    status = Column(String, default='active')

    notifications = relationship("Notification", back_populates="user")

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    address = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    medical_history = Column(String, nullable=True)

    appointments = relationship("Appointment", back_populates="patient")

class PatientProfile(Base):
    __tablename__ = 'patient_profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_of_birth = Column(Date)
    gender = Column(String)
    address = Column(String)
    medical_history = Column(String, nullable=True)

    user = relationship("User", backref=backref("patient_profile", uselist=False))

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    specialty = Column(String)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    photo_url = Column(String, nullable=True)

    appointments = relationship("Appointment", back_populates="doctor")
    reviews = relationship("Review", back_populates="doctor")
    schedules = relationship("HospitalSchedule", back_populates="doctor")

class DoctorProfile(Base):
    __tablename__ = 'doctor_profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    specialty = Column(String)
    bio = Column(String, nullable=True)
    qualifications = Column(String, nullable=True)
    experience_years = Column(Integer, nullable=True)
    consultation_fee = Column(Float, nullable=True)
    availability = Column(JSON, nullable=True)
    
    user = relationship("User", backref=backref("doctor_profile", uselist=False))

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date)
    time = Column(String)
    status = Column(String, default='UPCOMING')
    reason = Column(String)
    notes = Column(String, nullable=True)
    review_given = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)

    patient = relationship("Patient", back_populates="appointments", lazy="joined")
    doctor = relationship("Doctor", back_populates="appointments", lazy="joined")
    consultation = relationship("Consultation", back_populates="appointment", uselist=False)
    review = relationship("Review", back_populates="appointment", uselist=False)
    transaction = relationship("Transaction", back_populates="appointment", uselist=False)

    @property
    def patient_name(self):
        return self.patient.name if self.patient else ""

    @property
    def patient_photo(self):
        return self.patient.photo_url if self.patient else ""

    @property
    def doctor_name(self):
        return self.doctor.name if self.doctor else ""

    @property
    def doctor_photo(self):
        return self.doctor.photo_url if self.doctor else ""

    @property
    def doctor_specialty(self):
        return self.doctor.specialty if self.doctor else ""

class Consultation(Base):
    __tablename__ = 'consultations'
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    subjective = Column(String)
    objective = Column(String)
    assessment = Column(String)
    plan = Column(String)
    prognosis = Column(String, nullable=True)

    appointment = relationship("Appointment", back_populates="consultation")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    rating = Column(Float)
    comment = Column(String)
    date = Column(DateTime)

    appointment = relationship("Appointment", back_populates="review")
    doctor = relationship("Doctor", back_populates="reviews")

class Hospital(Base):
    __tablename__ = 'hospitals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    departments = Column(String)
    website = Column(String)
    phone_no = Column(String)
    current_status = Column(String)
    image = Column(String)
    timings = Column(String)

    schedules = relationship("HospitalSchedule", back_populates="hospital")

class HospitalSchedule(Base):
    __tablename__ = 'hospital_schedules'
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    consultationFee = Column(Float)
    availability = Column(JSON)

    hospital = relationship("Hospital", back_populates="schedules")
    doctor = relationship("Doctor", back_populates="schedules")

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True, index=True)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    amount = Column(Float)
    status = Column(String, default='PENDING')
    payment_method = Column(String)
    transaction_date = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="transaction")
