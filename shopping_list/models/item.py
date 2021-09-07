import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from .base import Model


class Item(Model):
    __tablename__ = 'item'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(256))
    order = Column(Integer)
    list_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('list.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    list = relationship('List', back_populates='items')
