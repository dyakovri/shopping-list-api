from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.orm import make_transient
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from shopping_list.models import List, User
from shopping_list.schemas import UserGet


router = APIRouter()


@cbv(router)
class UserHandler:
    @router.post('/', response_model=UserGet, status_code=status.HTTP_201_CREATED)
    def create_user(self):
        session = db.session
        user = User(lists=[List()])
        session.add(user)
        session.commit()
        return user

    @router.get(
        '/{user_id}',
        response_model=UserGet,
        status_code=status.HTTP_200_OK,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'User not found'}},
    )
    def get_user(self, user_id: UUID4 = Query(None, description='User ID')):
        session = db.session
        try:
            lst = session.query(User).filter(User.user_id == user_id).one()
        except NoResultFound:
            raise HTTPException(404, "User not found")
        return lst
