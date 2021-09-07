from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from shopping_list.models.item import Item
from shopping_list.schemas import ItemCreate, ItemGet, ItemUpdate


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
        self, item_in: ItemCreate, list_id: UUID4 = Query(None, description='Shopping list ID')
    ):
        session = db.session
        try:
            item = Item(name=item_in.name, order=item_in.order, list_id=list_id)
            session.add(item)
        except IntegrityError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'List not found')
        session.commit()
        return item

    @router.patch(
        '/{item_id}',
        response_model=ItemGet,
        status_code=status.HTTP_202_ACCEPTED,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'Item not found'}},
    )
    def change_item(
        self,
        item_in: ItemUpdate,
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        session = db.session
        try:
            item = (
                session.query(Item).filter(Item.item_id == item_id).filter(Item.list_id == list_id).one()
            )
        except NoResultFound:
            raise HTTPException(404, "Item not found")
        item = Item(item_id=item_id, list_id=list_id, **item_in.dict(exclude_unset=True))
        item = session.merge(item)
        session.commit()
        return item

    @router.delete(
        '/{item_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        responses={status.HTTP_404_NOT_FOUND: {'details': 'Item not found'}},
    )
    def delete_item(
        self,
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        session = db.session
        try:
            item = (
                session.query(Item).filter(Item.item_id == item_id).filter(Item.list_id == list_id).one()
            )
        except NoResultFound:
            raise HTTPException(404, "Item not found")
        session.delete(item)
        session.commit()
        return item
