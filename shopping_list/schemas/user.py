from typing import List

from pydantic.types import UUID4

from .base import BaseSchema
from .list import ShoppingList


class User(BaseSchema):
    user_id: UUID4


class UserGet(User):
    lists: List[ShoppingList]
