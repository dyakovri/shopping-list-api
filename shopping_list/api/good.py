from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from shopping_list.schemas import GoodRequest, GoodListGet

router = APIRouter()


@cbv(router)
class GoodHandler:
    @router.get('/good', response_model=GoodListGet)
    def get_recommendation(self, good_in: GoodRequest) -> GoodListGet:
        return {}
