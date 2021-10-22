import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime, String

from .base import BaseModel


class List(BaseModel):
    __tablename__ = 'list'

    list_id = Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, default='New shopping list', nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship('User', back_populates='lists', secondary='list_user_link')
    items = relationship('Item', back_populates='list', order_by='Item.order')
    sharings = relationship('Share', back_populates='list')
