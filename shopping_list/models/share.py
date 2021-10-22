import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from shopping_list.schemas import SharingOptions

from .base import BaseModel


class Share(BaseModel):
    __tablename__ = 'share'

    share_id = Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    share_type = Column(postgresql.ENUM(SharingOptions), nullable=False)
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    list_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('list.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    list = relationship('List', back_populates='sharings')
    user = relationship('User', back_populates='sharings')
