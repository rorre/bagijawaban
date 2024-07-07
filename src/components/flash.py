from likulau.hooks import use_request


def use_flash():
    request = use_request()
    flashes: list[str] = request.session.get("flash", [])
    request.session["flash"] = []
    return flashes


def flash(message: str):
    request = use_request()

    flashes = request.session.get("flash", [])
    flashes.append(message)

    request.session["flash"] = flashes
