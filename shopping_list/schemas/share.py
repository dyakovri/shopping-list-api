from enum import Enum
from typing import Optional

from pydantic.networks import AnyHttpUrl
from pydantic.types import UUID4

from .base import BaseSchema


class SharingOptions(str, Enum):
    RO = 'ro'
    RW = 'rw'


class CreateShare(BaseSchema):
    type: SharingOptions


class CreateShareResponse(BaseSchema):
    share_id: UUID4
    link: AnyHttpUrl
    qr: AnyHttpUrl
    type: SharingOptions
    user_id: Optional[UUID4]
    list_id: Optional[UUID4]
