from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from shopping_list.models import Fave, Item, List, ListUserLink, User
from shopping_list.schemas import ListGet


router = APIRouter()


@cbv(router)
class ListHandler:
    @router.post('/', response_model=ListGet, status_code=status.HTTP_201_CREATED)
    def create_list(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
    ):
        session = db.session
        try:
            user: User = session.query(User).filter(User.user_id == user_id).one()
        except NoResultFound:
            raise HTTPException(404, "List not found")
        list = List()
        session.add(list)
        user.lists.append(list)
        session.commit()
        return list

    @router.get(
        '/{list_id}',
        response_model=ListGet,
        status_code=status.HTTP_200_OK,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'List not found'}},
    )
    def get_list(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
    ):
        session = db.session
        try:
            lst = (
                session.query(List)
                .join(ListUserLink, User)
                .filter(User.user_id == user_id, List.list_id == list_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "List not found")
        items = (
            session.query(Item.item_id, Item.name, Item.check, Fave.fave_id)
            .outerjoin(Fave, Fave.name == Item.name)
            .order_by(Item.order)
            .all()
        )
        return {'list_id': lst.list_id, 'name': lst.name, 'items': items}

    @router.post(
        '/{list_id}/checkall',
        response_model=ListGet,
        status_code=status.HTTP_200_OK,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'List not found'}},
    )
    def mark_bought(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
    ):
        session = db.session
        try:
            lst = (
                session.query(List)
                .join(ListUserLink, User)
                .filter(User.user_id == user_id, List.list_id == list_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "List not found")
        for item in lst.items:
            item.check = True
        session.commit()
        return lst
