from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from shopping_list import __version__
from shopping_list.api import good_router, item_router, list_router, user_router
from shopping_list.base.settings import get_settings


settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title='Shopping list API',
        description='DIPD project. Shopping list app.',
        version=__version__,
        openapi_prefix=settings.OPENAPI_PREFIX,
    )
    app.include_router(user_router, prefix='/users', tags=['User'])
    app.include_router(good_router, prefix='/users/{user_id}/goods', tags=['Autocomplete'])
    app.include_router(list_router, prefix='/users/{user_id}/lists', tags=['List'])
    app.include_router(item_router, prefix='/users/{user_id}/lists/{list_id}/items', tags=['Item'])
    app.add_middleware(
        middleware_class=DBSessionMiddleware,
        db_url=settings.DB_DSN,
        engine_args={'pool_pre_ping': True},
        session_args={'autocommit': False, 'autoflush': False},
    )
    return app
