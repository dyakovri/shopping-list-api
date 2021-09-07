from fastapi import APIRouter
from fastapi_utils.cbv import cbv


router = APIRouter()

@cbv(router)
class ItemHandler:
    @router.post('/{list_id}')
    def create_item(self, list_id: str):
        return {}

    @router.patch('/{list_id}/{item_id}')
    def change_item(self, list_id: str, item_id: str):
        return {}

    @router.delete('/{list_id}/{item_id}')
    def delete_item(self, list_id: str, item_id: str):
        return {}
