from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base

class User_Group(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
