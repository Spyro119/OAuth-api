from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.base_class import Base

class Token(Base):
    __tablename__ = "token"
    access_token = Column(String, nullable=False, index=True, primary_key=True)
    refresh_token = Column(String, nullable=False)
    expires_in = Column(DateTime(timezone=False), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User")