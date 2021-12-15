from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import func
from starlette.status import HTTP_204_NO_CONTENT

from shopping_list.models import Fave, Item, List, ListUserLink, User
from shopping_list.schemas import GoodListGet
from shopping_list.schemas.good import FaveListGet, HistoryListGet


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

    @router.get('/history', response_model=HistoryListGet)
    def get_history(self, user_id):
        session = db.session
        hist_items = (
            session.query(Item.name, Item.list_id, Item.item_id, Fave.fave_id)
            .outerjoin(Fave, Fave.name == Item.name)
            .join(List, ListUserLink, User)
            .filter(User.user_id == user_id, Item.check)
            .order_by(Item.updated_at)
            .distinct()
            .all()
        )
        return {'items': hist_items}

    @router.get('/favourites', response_model=FaveListGet)
    def get_favourites(self, user_id):
        session = db.session
        hist_items = (
            session.query(Fave.name, Fave.fave_id)
            .filter(Fave.user_id == user_id)
            .order_by(Fave.name)
            .all()
        )
        return {'items': hist_items}

    @router.delete('/favourites/{fave_id}', status_code=HTTP_204_NO_CONTENT)
    def delete_favourite(self, user_id, fave_id):
        session = db.session
        try:
            fave_item = (
                session.query(Fave)
                .filter(Fave.user_id == user_id, Fave.fave_id == fave_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "List not found")
        session.delete(fave_item)
        session.commit()
