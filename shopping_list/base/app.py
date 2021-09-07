from fastapi import FastAPI
from shopping_list import __version__
from shopping_list.api import item_router, list_router, good_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Shopping list API',
        description='DIPD project. Shopping list app.',
        version=__version__,
    )
    app.include_router(list_router, prefix='/lists', tags=['List'])
    app.include_router(item_router, prefix='/lists/{list_id}/items', tags=['Item'])
    app.include_router(good_router, tags=['Recommendations'])
    return app

