from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False, length=50)
    first_name = Column(String, index=True, length=50)
    last_name = Column(String, index=True, length=50)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False, length=256)
    password_changed = Column(String, nullable=False, default=False, length=5)
    password_expiration_delay = Column(Integer, default=30)
    password_expired = Column(Boolean, default=True)
    password_reset_link = Column(String, nullable=True, length=256)
    is_active = Column(Boolean(), default=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    date_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    groups = relationship("Group", secondary="user_groups", back_populates="users")