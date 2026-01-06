from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user = relationship('User', back_populates='transactions')
