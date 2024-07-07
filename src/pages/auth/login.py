from likulau.hooks import use_request

from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from src.components.flash import flash
from src.db import get_db_conn
from src.external.cas import CASClient


async def page() -> RedirectResponse:
    request = use_request()
    cas = CASClient(str(request.base_url) + "auth/login")
    ticket = request.query_params.get("ticket", "")
    if not ticket:
        return RedirectResponse(cas.login_url)

    try:
        response = await cas.authenticate(ticket)
        data = response.get("serviceResponse", {})
        if "authenticationSuccess" not in data:
            raise Exception("SSO failed")
    except Exception:
        raise HTTPException(detail="Cannot authenticate with SSO", status_code=401)

    data = data["authenticationSuccess"]
    if "npm" not in data["attributes"]:
        raise HTTPException(detail="Cannot authenticate with SSO", status_code=401)

    attributes = data["attributes"]

    db = await get_db_conn()
    await db.execute(
        "INSERT INTO users(npm, username, name) VALUES (?, ?, ?) ON CONFLICT (npm) DO UPDATE SET username = EXCLUDED.username, name = EXCLUDED.name",
        (int(attributes["npm"]), data["user"], attributes["nama"]),
    )

    request.session["id"] = int(attributes["npm"])
    flash("Successfully logged in!")
    return RedirectResponse("/")
