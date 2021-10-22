from typing import List

from pydantic.types import UUID4

from .base import BaseSchema
from .item import ItemGet


class ShoppingList(BaseSchema):
    list_id: UUID4
    name: str


class ListGet(ShoppingList):
    items: List[ItemGet]
