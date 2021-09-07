from typing import List, Optional

from pydantic import Field
from pydantic.types import UUID4

from .base import BaseSchema
from .item import ItemGet


class ShoppingList(BaseSchema):
    pass


class ListGet(ShoppingList):
    list_id: UUID4
    items: List[ItemGet]
