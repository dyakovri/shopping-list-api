from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from shopping_list import __version__
from shopping_list.api import item_router, list_router, share_router, tips_router, user_router
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
    app.include_router(tips_router, prefix='/users/{user_id}', tags=['Autocomplete'])
    app.include_router(list_router, prefix='/users/{user_id}/lists', tags=['List'])
    app.include_router(item_router, prefix='/users/{user_id}/lists/{list_id}/items', tags=['Item'])
    app.include_router(share_router, tags=['Share'])
    app.add_middleware(
        middleware_class=DBSessionMiddleware,
        db_url=settings.DB_DSN,
        engine_args={'pool_pre_ping': True},
        session_args={'autocommit': False, 'autoflush': False},
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
