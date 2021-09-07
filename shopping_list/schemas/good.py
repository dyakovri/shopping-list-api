from typing import List, Optional

from pydantic import Field

from .base import BaseSchema


class Good(BaseSchema):
    pass


class GoodGet(Good):
    name: Optional[str] = Field(None, description="Recomendations for request", example="Milk 1l")


class GoodListGet(BaseSchema):
    query: str = Field(None, description="Recomendation request", example="Mil")
    items: List[GoodGet]
