from fastapi import FastAPI
from shopping_list import __version__
from shopping_list.api import ItemRouter, ListRouter, GoodRouter

def create_app() -> FastAPI:
    app = FastAPI(
        title='Shopping list API',
        description='DIPD project. Shopping list app.',
        version=__version__,
    )
    app.include_router(ItemRouter, tags=['Item'])
    app.include_router(ListRouter, tags=['List'])
    app.include_router(GoodRouter, tags=['Recommendations'])
    return app

