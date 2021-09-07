from typing import List, Optional

from pydantic import Field
from pydantic.types import UUID4

from .base import BaseSchema


class Item(BaseSchema):
    name: str = Field(None, description='Item test', example="Milk 1l")


class ItemGet(Item):
    item_id: UUID4
    check: Optional[bool] = Field(None, description='Is bought check', example=True)


class ItemCreate(Item):
    pass


class ItemUpdate(Item):
    check: Optional[bool] = Field(None, description='Is bought check', example=True)
