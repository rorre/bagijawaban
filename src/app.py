from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware

from likulau.env import env

from src.db import setup_database


@asynccontextmanager
async def lifespan(app: Starlette):
    await setup_database()
    yield


def app(app: Starlette):
    app.add_middleware(
        SessionMiddleware,
        secret_key=env("SECRET_KEY"),
        https_only=True,
        same_site="strict",
    )
    return app
