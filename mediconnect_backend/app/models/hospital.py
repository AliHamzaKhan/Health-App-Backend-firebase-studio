from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    departments = Column(String)
    website = Column(String)
    phone_no = Column(String)
    current_status = Column(String)
    image = Column(String)
    timings = Column(String)
