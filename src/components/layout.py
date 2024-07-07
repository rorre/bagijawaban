import liku as e

from src.providers.auth import use_current_user
from src.components.flash import use_flash


def Navbar():
    user = use_current_user()
    return e.nav(
        props={"class_": "flex flex-col md:flex-row p-4 justify-between gap-4 bg-base-200"},
        children=[
            e.a(
                props={"href": "/"},
                children=e.strong(
                    props={"class_": "font-bold text-lg"},
                    children="BagiJawaban",
                ),
            ),
            e.div(
                props={"class_": "flex flex-col md:flex-row gap-4"},
                children=[
                    e.a(props={"href": "/course", "class_": "hover:link-hover"}, children="Courses"),
                    e.div(props={"class_": "hidden md:divider md:divider-horizontal md:mx-0"}),
                    *(
                        [
                            e.p(props={"class_": "opacity-75"}, children=f"Hello, {user.name}"),
                            e.a(props={"href": "/auth/logout", "class_": "hover:link-hover"}, children="Log out"),
                        ]
                        if user
                        else [e.a(props={"href": "/auth/login", "class_": "hover:link-hover"}, children="Log in")]
                    ),
                ],
            ),
        ],
    )


def Layout(children: e.HTMLElement):
    flashes = use_flash()
    return e.html(
        children=[
            e.head(
                children=[
                    e.meta(props={"charset": "UTF-8"}),
                    e.meta(
                        props={
                            "name": "viewport",
                            "content": "width=device-width, initial-scale=1.0",
                        }
                    ),
                    e.title(children="BagiJawaban"),
                    e.link(
                        props={
                            "href": "/static/css/style.css",
                            "rel": "stylesheet",
                            "type": "text/css",
                        }
                    ),
                ]
            ),
            Navbar(),
            e.main(
                props={"class_": "container mx-auto px-8"},
                children=[
                    *[
                        e.div(props={"role": "alert", "class_": "alert alert-info my-4"}, children=e.span(children=msg))
                        for msg in flashes
                    ],
                    children,
                ],
            ),
        ]
    )
