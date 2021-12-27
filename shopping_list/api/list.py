from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query, Body
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from shopping_list.models import Fave, Item, List, ListUserLink, User
from shopping_list.schemas import ListGet, ListCreate


router = APIRouter()


@cbv(router)
class ListHandler:
    @router.post('/', response_model=ListGet, status_code=status.HTTP_201_CREATED)
    def create_list(
        self,
        list_args: ListCreate,
        user_id: UUID4 = Query(None, description='User ID'),
    ):
        session = db.session
        try:
            user: User = session.query(User).filter(User.user_id == user_id).one()
        except NoResultFound:
            raise HTTPException(404, "List not found")
        lst = List(name=list_args.name)
        session.add(lst)
        user.lists.append(lst)
        session.commit()
        return {'list_id': lst.list_id, 'name': lst.name, 'items': lst.items, 'read_only': False}

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
            lst, read_only = (
                session.query(List, ListUserLink.read_only)
                .join(ListUserLink, User)
                .filter(User.user_id == user_id, List.list_id == list_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "List not found")
        items = (
            session.query(Item.item_id, Item.name, Item.check, Fave.fave_id)
            .join(List, ListUserLink)
            .outerjoin(Fave, Fave.name == Item.name)
            .filter(User.user_id == user_id, ListUserLink.list_id == list_id)
            .order_by(Item.order)
            .distinct()
            .all()
        )
        return {'list_id': lst.list_id, 'name': lst.name, 'items': items, 'read_only': read_only}

    @router.delete(
        '/{list_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'List not found'}},
    )
    def delete_list(
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
        session.delete(lst)
        session.commit()

    @router.post(
        '/{list_id}/checkall',
        response_model=ListGet,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_404_NOT_FOUND: {'details': 'List not found'},
            status.HTTP_403_FORBIDDEN: {'detail': 'Can not edit readonly list'},
        },
    )
    def mark_bought(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
    ):
        session = db.session
        try:
            lst, read_only = (
                session.query(List, ListUserLink.read_only)
                .join(ListUserLink, User)
                .filter(User.user_id == user_id, List.list_id == list_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "List not found")
        if read_only:
            raise HTTPException(403, "Can not edit readonly list")
        for item in lst.items:
            item.check = True
        session.commit()
        return {'list_id': lst.list_id, 'name': lst.name, 'items': lst.items, 'read_only': read_only}
