from functools import lru_cache
from typing import Any

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from returns.pipeline import pipe
from starlette.middleware.cors import CORSMiddleware
from app.controller import meta_controller as meta
from app.domain import sync_domain
from app.util import ddl

from app.util.logger import get_logger


_START_EVENT = "startup"
_LOG = get_logger(__name__.split(".")[-1])


def _setup_cors(app: FastAPI) -> FastAPI:
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


@lru_cache
def _setup_app() -> FastAPI:
    app = FastAPI(**{"title": "Studio Sync SG Client", "version": "0.0.1"})
    app.include_router(meta.router)
    # app.include_router(client.router)
    return app


@lru_cache
def _setup_tasks(app: FastAPI) -> FastAPI:
    @app.on_event("startup")
    @repeat_every(seconds=45)
    async def synchronize_data() -> Any:
        _LOG.info("Start synchronization")
        await sync_domain.synchronize_all()

    @app.on_event("startup")
    async def bootstrap_db() -> Any:
        _LOG.info("Setup database")
        await ddl.setup_db()

    return app


setup_all = pipe(lambda _: _setup_app(), _setup_cors, _setup_tasks)

