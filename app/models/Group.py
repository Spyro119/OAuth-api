from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True, length=25)
    description = Column(String, length=256)
    is_active = Column(Boolean, default=True)

    users = relationship("User", secondary="user_groups", back_populates="groups")
    permissions = relationship('Permission', secondary='permission_groups', back_populates='groups')