from fastapi import APIRouter
from fastapi_utils.cbv import cbv


router = APIRouter()


@cbv(router)
class ItemHandler:
    @router.post('/')
    def create_item(self, list_id: str):
        return {}

    @router.patch('/{item_id}')
    def change_item(self, list_id: str, item_id: str):
        return {}

    @router.delete('/{item_id}')
    def delete_item(self, list_id: str, item_id: str):
        return {}
