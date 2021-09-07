from fastapi import APIRouter
from fastapi.params import Query
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from shopping_list.schemas import ListGet
from starlette import status

router = APIRouter()


@cbv(router)
class ListHandler:
    @router.post('/', response_model=ListGet)
    def create_list(self):
        pass

    @router.get('/{list_id}', response_model=ListGet)
    def get_list(
        self,
        list_id: UUID4 = Query(None, description='Shopping list ID')
    ):
        pass

    @router.post('/{list_id}:share', response_model=ListGet)
    def share_list(
        self,
        list_id: UUID4 = Query(None, description='Shopping list ID')
    ):
        pass

    @router.post('/{list_id}:checkall', status_code=status.HTTP_200_OK)
    def mark_bought(
        self,
        list_id: UUID4 = Query(None, description='Shopping list ID')
    ):
        pass
