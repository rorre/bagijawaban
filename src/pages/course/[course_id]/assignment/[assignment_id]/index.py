from typing import cast
import liku as e
from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.components.button import LinkButton
from src.components.card import Card
from src.providers.auth import use_current_user
from src.components.solution import SubmitSolution, SolutionsList
from src.components.layout import Layout
from src.models import Assignment
from src.db import query

import mistune

layout = Layout


async def get_ssr_props(request: Request) -> Assignment | None:
    try:
        assignment = (
            await query(
                "SELECT * FROM assignments WHERE course_id = ? AND id = ?",
                (request.path_params["course_id"], request.path_params["assignment_id"]),
                cls=Assignment,
            )
        )[0]
        assignment.description = cast(str, mistune.html(assignment.description))
        return assignment
    except IndexError:
        return None


async def page(props: Assignment | None):
    current_user = use_current_user()

    if not props:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return e.div(
        props={"class_": "flex flex-col gap-4 py-8"},
        children=[
            e.h1(
                props={"class_": "text-3xl font-bold"},
                children=props.name,
            ),
            e.div(
                props={"class_": "flex flex-col lg:flex-row gap-4"},
                children=[
                    e.article(
                        props={"class_": "prose xl:prose-xl w-full !max-w-none basis-3/5"},
                        children=props.description,
                        safe=True,
                    ),
                    e.div(
                        props={"class_": "flex flex-col gap-2 basis-2/5"},
                        children=(
                            [
                                SubmitSolution(props.id),
                                (await SolutionsList(props.id)),
                            ]
                            if current_user
                            else Card(
                                title=e.p(children="You are not logged in"),
                                body="Log in to see and submit solutions",
                                actions=LinkButton("/auth/login", "Log in with SSO"),
                                class_="!text-center bg-neutral !items-center !justify-center",
                                actions_class_="justify-center",
                            )
                        ),
                    ),
                ],
            ),
        ],
    )
