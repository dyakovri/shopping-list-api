from fastapi import APIRouter
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import query
from sqlalchemy.sql.functions import func

from shopping_list.models import Item, List
from shopping_list.schemas import GoodListGet


router = APIRouter()


@cbv(router)
class GoodHandler:
    @router.get('/good', response_model=GoodListGet)
    def get_recommendation(
        self, user_id, query: str = Query(None, description="Part of good name", example="Mil")
    ) -> GoodListGet:
        session = db.session
        goods = session.query(Item.name).join(List).filter(List.user_id == user_id).limit(5).all()
        return {'query': query, 'items': goods}
