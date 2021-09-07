import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql

from .base import Model


class Good(Model):
    __tablename__ = 'good'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(256))
