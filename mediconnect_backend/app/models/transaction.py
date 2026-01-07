from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ matches User.__tablename__
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="transactions")

