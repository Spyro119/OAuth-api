from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    password_changed = Column(String(5), nullable=False, default=False)
    password_expiration_delay = Column(Integer, default=30)
    password_expired = Column(Boolean, default=True)
    password_reset_link = Column(String(256), nullable=True)
    is_active = Column(Boolean(), default=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    date_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    groups = relationship("Group", secondary="user_groups", back_populates="users")