from fastapi import APIRouter
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import query
from sqlalchemy.sql.functions import func

from shopping_list.models import Good
from shopping_list.schemas import GoodListGet


router = APIRouter()


@cbv(router)
class GoodHandler:
    @router.get('/good', response_model=GoodListGet)
    def get_recommendation(
        self, query: str = Query(None, description="Recomendation request", example="Mil")
    ) -> GoodListGet:
        session = db.session
        goods = session.query(Good)
        goods = goods.filter(func.lower(Good.name).startswith(query.lower()))
        goods = goods.limit(3).all()
        return {'query': query, 'items': goods}
