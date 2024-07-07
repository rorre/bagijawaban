import liku as e
from dataclasses import dataclass

from src.components.layout import Layout
from src.components.button import LinkButton
from src.components.card import Card
from src.db import query
from src.models import Assignment
from starlette.requests import Request


@dataclass
class AssignmentPageProps:
    course_id: str
    assignments: list[Assignment]


layout = Layout


async def get_ssr_props(request: Request) -> AssignmentPageProps:
    course_id = request.path_params["course_id"]
    assignments = await query(
        "SELECT * FROM assignments WHERE course_id = ?",
        [course_id],
        cls=Assignment,
    )
    return AssignmentPageProps(course_id, assignments)


def page(props: AssignmentPageProps):
    cards = []
    for assignment in props.assignments:
        description = assignment.description
        try:
            description = description[: assignment.description.index("\n")]
        except ValueError:
            pass

        cards.append(
            Card(
                assignment.name,
                e.p(children=description),
                LinkButton(f"/course/{props.course_id}/assignment/{assignment.id}", "Detail"),
                class_="bg-neutral",
            )
        )

    return e.div(
        props={"class_": "flex flex-col gap-4 py-8"},
        children=[
            e.h1(
                props={
                    "class_": "text-3xl font-bold",
                },
                children="Assignments",
            ),
            e.div(
                props={"class_": "grid grid-cols-1 md:grid-cols-2 gap-4"},
                children=cards,
            ),
        ],
    )
