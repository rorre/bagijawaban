import liku as e

from src.providers.auth import use_current_user
from src.components.layout import Layout


def layout(_props: None, children: e.HTMLElement):
    return Layout("Index", children)


def page() -> e.HTMLElement:
    current_user = use_current_user()
    return e.div(
        props={"class_": "prose py-8 mx-auto"},
        children=[
            e.h1(props={"class_": "text-3xl font-bold"}, children="Welcome to BagiJawaban!"),
            e.p(
                children="A place where everyone in CSUI can share their past assignments. Everyone is welcomed to contribute! "
                "Public can see all the assignments, whereas UI students are able to submit and see submissions by other people."
            ),
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
            e.div(
                props={"class_": "rounded-lg bg-neutral"},
                children=[
                    e.div(
                        props={"class_": "alert alert-info !rounded-b-none"},
                        children=[
                            e.Fragment(
                                children="""<svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            class="h-6 w-6 shrink-0 stroke-current">
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            </svg>""",
                                safe=True,
                            ),
                            e.strong(props={"class_": "font-bold text-info-content"}, children="Volunteer required!"),
                        ],
                    ),
                    e.p(
                        props={"class_": "px-4"},
                        children="We are looking for volunteers from any generation (regardless of whether you are 2022, 2021, or above) to"
                        "convert all of the lab assignments during your time to markdown, so we can publish it in this site!",
                    ),
                    e.p(
                        props={"class_": "px-4 pb-4"},
                        children="If you are interested, please contact @ro_rre on Twitter/X.",
                    ),
                ],
            ),
        ],
    )
