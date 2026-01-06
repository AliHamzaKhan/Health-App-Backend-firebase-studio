from sqlalchemy import Column, Integer, String, Float, ARRAY
from app.db.base_class import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    features = Column(ARRAY(String))
