from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.orm import make_transient
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from shopping_list.models import Item, List
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
        list = List(user_id=user_id)
        session.add(list)
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
                session.query(List).filter(List.user_id == user_id).filter(List.list_id == list_id).one()
            )
            # TODO: In favourites
        except NoResultFound:
            raise HTTPException(404, "List not found")
        return lst

    # TODO: Sharing
    # @router.post('/{list_id}:share', response_model=ListGet, status_code=status.HTTP_200_OK)
    # def share_list(
    #     self,
    #     user_id: UUID4 = Query(None, description='User ID'),
    #     list_id: UUID4 = Query(None, description='Shopping list ID'),
    # ):
    #     session = db.session
    #     try:
    #         lst = (
    #             session.query(List).filter(List.user_id == user_id).filter(List.list_id == list_id).one()
    #         )
    #     except NoResultFound:
    #         raise HTTPException(404, "List not found")
    #     new_lst = List()
    #     session.add(new_lst)
    #     for i, item in enumerate(lst.items):
    #         if item.check:
    #             continue
    #         item = Item(name=item.name, order=i, check=item.check)
    #         session.add(item)
    #         new_lst.items.append(item)
    #     session.commit()
    #     return new_lst

    @router.post(
        '/{list_id}:checkall',
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
                session.query(List).filter(List.user_id == user_id).filter(List.list_id == list_id).one()
            )
        except NoResultFound:
            raise HTTPException(404, "List not found")
        for item in lst.items:
            item.check = True
        session.commit()
        return lst
