import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from shopping_list.models import Fave, Item, List, User
from shopping_list.schemas import ItemCreate, ItemGet, ItemUpdate


logging.basicConfig(level=logging.DEBUG)
router = APIRouter()


@cbv(router)
class ItemHandler:
    @router.post(
        '/',
        response_model=ItemGet,
        status_code=status.HTTP_201_CREATED,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'List not found'}},
    )
    def create_item(
        self,
        item_in: ItemCreate,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
    ):
        session = db.session
        try:
            lst = (
                session.query(List).filter(List.user_id == user_id).filter(List.list_id == list_id).one()
            )
            item = Item(name=item_in.name, order=item_in.order, list_id=lst.list_id)
            session.add(item)
        except (NoResultFound, IntegrityError):
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'List not found')
        session.commit()
        # Is item in faves
        fave: Fave = (
            session.query(Fave).filter(Fave.user_id == user_id, Fave.name == item.name).one_or_none()
        )
        fave_id = fave.fave_id if fave else None
        return {'name': item.name, 'item_id': item.item_id, 'check': item.check, 'fave_id': fave_id}

    @router.patch(
        '/{item_id}',
        response_model=ItemGet,
        status_code=status.HTTP_202_ACCEPTED,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'Item not found'}},
    )
    def change_item(
        self,
        item_in: ItemUpdate,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        session = db.session
        try:
            item = (
                session.query(Item)
                .join(List, User)
                .filter(User.user_id == user_id, List.list_id == list_id, Item.item_id == item_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "Item not found")
        item = Item(item_id=item_id, list_id=list_id, **item_in.dict(exclude_unset=True))
        item = session.merge(item)
        session.commit()
        # Is item in faves
        fave: Fave = (
            session.query(Fave).filter(Fave.user_id == user_id, Fave.name == item.name).one_or_none()
        )
        fave_id = fave.fave_id if fave else None
        return {'name': item.name, 'item_id': item.item_id, 'check': item.check, 'fave_id': fave_id}

    @router.delete(
        '/{item_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'Item not found'}},
    )
    def delete_item(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        session = db.session
        try:
            item = (
                session.query(Item)
                .join(List, User)
                .filter(User.user_id == user_id, List.list_id == list_id, Item.item_id == item_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "Item not found")
        session.delete(item)
        session.commit()

    @router.post(
        '/{item_id}/fave',
        response_model=ItemGet,
        status_code=status.HTTP_202_ACCEPTED,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'Item not found'}},
    )
    def fave_item(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        session = db.session
        try:
            item: Item = (
                session.query(Item)
                .join(List, User)
                .filter(Item.item_id == item_id, List.list_id == list_id, User.user_id == user_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "Item not found")
        try:
            logging.debug(f'Trying to find {item.name} in faves')
            fave: Fave = (
                session.query(Fave).filter(Fave.user_id == user_id, Fave.name == item.name).one()
            )
        except NoResultFound:
            logging.debug(f'No {item.name} found in faves. Adding.')
            fave = Fave(user_id=user_id, name=item.name)
            session.add(fave)
            session.commit()
        return {'name': item.name, 'item_id': item.item_id, 'check': item.check, 'fave_id': fave.fave_id}

    @router.delete(
        '/{item_id}/fave',
        response_model=ItemGet,
        status_code=status.HTTP_202_ACCEPTED,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'Item not found'}},
    )
    def unfave_item(
        self,
        user_id: UUID4 = Query(None, description='User ID'),
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        session = db.session
        try:
            item: Item = (
                session.query(Item)
                .join(List, User)
                .filter(Item.item_id == item_id, List.list_id == list_id, User.user_id == user_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(404, "Item not found")
        fave: Fave = session.query(Fave).filter(Fave.user_id == user_id, Fave.name == item.name).delete()
        session.commit()
        return {'name': item.name, 'item_id': item.item_id, 'check': item.check}
