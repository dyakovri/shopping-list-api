import logging

from fastapi import APIRouter, status
from fastapi.params import Query
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from shopping_list.schemas import ItemCreate, ItemGet, ItemUpdate

router = APIRouter()


@cbv(router)
class ItemHandler:
    @router.post('/', response_model=ItemGet, status_code=status.HTTP_201_CREATED)
    def create_item(
        self,
        item_in: ItemCreate,
        list_id: UUID4 = Query(None, description='Shopping list ID')
    ):
        logging.debug({
            'item_in': item_in.dict(),
            'list_id': list_id,
        })
        return {}

    @router.patch('/{item_id}', response_model=ItemGet, status_code=status.HTTP_202_ACCEPTED)
    def change_item(
        self,
        item_in: ItemUpdate,
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        logging.debug({
            'item_in': item_in.dict(),
            'list_id': list_id,
            'item_id': item_id,
        })
        return {}

    @router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(
        self,
        list_id: UUID4 = Query(None, description='Shopping list ID'),
        item_id: UUID4 = Query(None, description='Shopping list item ID'),
    ):
        logging.debug({
            'list_id': list_id,
            'item_id': item_id,
        })
        return {}
