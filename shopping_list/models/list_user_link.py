import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Boolean

from .base import BaseModel


class ListUserLink(BaseModel):
    __tablename__ = 'list_user_link'

    user_id = Column(ForeignKey('user.id'), primary_key=True)
    list_id = Column(ForeignKey('list.id'), primary_key=True)
    read_only = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
