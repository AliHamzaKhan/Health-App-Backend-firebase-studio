from sqlalchemy import Column, Integer, String, JSON
from app.db.base_class import Base

class RolePermission(Base):
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, unique=True, index=True, nullable=False)
    permissions = Column(JSON, nullable=False)
