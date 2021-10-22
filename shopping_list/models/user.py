import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    user_id = Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    lists = relationship(
        'List', back_populates='users', order_by='List.updated_at', secondary='list_user_link'
    )
    faves = relationship('Fave', back_populates='user', order_by='Fave.name')
    sharings = relationship('Share', back_populates='user')
