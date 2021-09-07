from fastapi import APIRouter
from fastapi_utils.cbv import cbv


router = APIRouter()

@cbv(router)
class ListHandler:
    @router.post('/')
    def create_list(self):
        pass

    @router.get('/{list_id}')
    def get_list(self, list_id: str):
        pass

    @router.post('/{list_id}/share')
    def share_list(self, list_id: str):
        pass

    @router.post('/{list_id}/checkall')
    def mark_bought(self, list_id: str):
        pass
