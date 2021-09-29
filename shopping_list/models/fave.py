import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, String

from .base import BaseModel


class Fave(BaseModel):
    __tablename__ = 'fave'

    fave_id = Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
    name = Column(String(256))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship('User', back_populates='faves')
