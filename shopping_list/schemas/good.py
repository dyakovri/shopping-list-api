from typing import List, Optional

from pydantic import Field
from pydantic.types import UUID4

from .base import BaseSchema


class Good(BaseSchema):
    name: Optional[str] = Field(None, description="Recomendations for request", example="Milk 1l")


class GoodGet(Good):
    pass


class GoodListGet(BaseSchema):
    query: str = Field(None, description="Recomendation request", example="Mil")
    items: List[GoodGet]


class HistoryGet(Good):
    item_id: Optional[UUID4] = Field(description='Id of item in list')
    list_id: Optional[UUID4] = Field(description='Id of list which item in')
    fave_id: Optional[UUID4] = Field(description='Id of fave if product in favourites list')


class HistoryListGet(BaseSchema):
    items: List[HistoryGet]


class FaveGet(Good):
    fave_id: Optional[UUID4] = Field(description='Id of fave if product in favourites list')


class FaveListGet(BaseSchema):
    items: List[FaveGet]
