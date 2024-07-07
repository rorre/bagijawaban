import liku as e
from liku.context import Context, use_context
from likulau.hooks import use_request

from likulau.providers import provider

from src.models import User
from src.db import query


context = Context[User | None]("auth")


@provider(context, [])
async def user_provider():
    req = use_request()
    try:
        user = (
            await query(
                "SELECT * FROM users WHERE npm = ? LIMIT 1",
                [req.session["id"]],
                cls=User,
            )
        )[0]
    except (IndexError, KeyError):
        user = None

    return context.provide(user)


def use_current_user():
    return use_context(context)
