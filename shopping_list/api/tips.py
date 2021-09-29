from fastapi import APIRouter
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import query
from sqlalchemy.sql.functions import func

from shopping_list.models import Item, List
from shopping_list.schemas import GoodListGet
from shopping_list.schemas.good import GoodGet


router = APIRouter()


@cbv(router)
class TipsHandler:
    @router.get('/tips', response_model=GoodListGet)
    def get_recommendation(
        self, user_id, query: str = Query(None, description="Part of good name", example="Mil")
    ) -> GoodListGet:
        session = db.session
        goods = (
            session.query(Item.name).join(List).filter(List.user_id == user_id).distinct().limit(5).all()
        )
        return {'query': query, 'items': goods}

    @router.get('/history', response_model=GoodListGet)
    def get_history(self, user_id):
        # TODO: Get history
        return

    @router.get('/favourites', response_model=GoodListGet)
    def get_favourites(self, user_id):
        # TODO: Get favourites
        return

    @router.delete('/favourites/{fave_id}', response_model=GoodGet)
    def delete_favourite(self, user_id, fave_id):
        # TODO: Drop from favourites
        return
