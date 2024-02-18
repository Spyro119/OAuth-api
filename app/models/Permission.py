from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String
from app.db.base_class import Base


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    group_name = Column(String)
    description = Column(String)
    version = Column(String)
    obsolete = Column(Boolean, default=False)
    sync_code = Column(String)
    obsolete_for_a_disabled_project = Column(Boolean, default=False)

    groups = relationship("Group", secondary="permission_groups", back_populates="permissions")