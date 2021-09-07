from fastapi import APIRouter
from fastapi_utils.cbv import cbv


router = APIRouter()


@cbv(router)
class GoodHandler:
    @router.get('/good')
    def get_recommendation(self):
        return {}
