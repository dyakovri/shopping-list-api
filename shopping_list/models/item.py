import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String

from .base import BaseModel


class Item(BaseModel):
    __tablename__ = 'item'

    item_id = Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    list_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('list.id'), primary_key=True)
    name = Column(String(256))
    order = Column(Integer)
    check = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    list = relationship('List', back_populates='items')
