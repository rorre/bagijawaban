import liku as e


def LinkButton(href: str, label: str, color: str = "btn-info", class_=""):
    return e.a(
        props={"href": href},
        children=e.button({"class_": "btn " + " ".join((color, class_))}, children=label),
    )
