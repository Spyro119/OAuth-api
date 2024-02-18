from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base

class Permission_group(Base):
    __tablename__ = 'permission_groups'
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))