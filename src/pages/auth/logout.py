from starlette.responses import RedirectResponse
from likulau.hooks import use_request


def page():
    request = use_request()
    if "id" in request.session:
        del request.session["id"]

    return RedirectResponse("/")
