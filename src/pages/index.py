import liku as e

from src.providers.auth import use_current_user
from src.components.layout import Layout


def layout(_props: None, children: e.HTMLElement):
    return Layout("Index", children)


def page() -> e.HTMLElement:
    current_user = use_current_user()
    return e.div(
        props={"class_": "space-y-2 py-8 mx-auto"},
        children=[
            e.h1(props={"class_": "text-3xl font-bold"}, children="Welcome to BagiJawaban!"),
            e.p(children="A place where everyone in CSUI can share their past assignments."),
            (
                e.a(
                    props={"href": "/auth/login"},
                    children=e.button(
                        props={"class_": "btn-info btn"},
                        children="Log in with SSO",
                    ),
                )
                if not current_user
                else None
            ),
        ],
    )
