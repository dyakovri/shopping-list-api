import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from .base import BaseModel


class List(BaseModel):
    __tablename__ = 'list'

    list_id = Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship('Item', back_populates='list', order_by='Item.order')
