from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Notification(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user = relationship('User', back_populates='notifications')
