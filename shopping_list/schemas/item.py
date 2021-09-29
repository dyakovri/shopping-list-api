from typing import List, Optional

from pydantic import Field
from pydantic.types import UUID4, conint

from .base import BaseSchema


class Item(BaseSchema):
    name: str = Field(None, description='Item test', example="Milk 1l")


class ItemGet(Item):
    item_id: UUID4
    check: Optional[bool] = Field(False, description='Is bought check', example=True)
    fave_id: Optional[UUID4] = Field(description='Id of fave if product in favourites list')


class ItemCreate(Item):
    order: conint(gt=0) = Field(None, description='Order num in list', example=1)


class ItemUpdate(Item):
    name: str = Field(None, description='Item test', example="Milk 1l")
    check: Optional[bool] = Field(None, description='Is bought check', example=True)
    order: conint(gt=0) = Field(None, description='Order num in list', example=1)
