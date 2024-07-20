import liku as e
from dataclasses import dataclass

from src.components.layout import Layout
from src.components.button import LinkButton
from src.components.card import Card
from src.db import query
from src.models import Assignment, Course

from starlette.exceptions import HTTPException
from starlette.requests import Request


@dataclass
class AssignmentPageProps:
    course: Course
    assignments: list[Assignment]


def layout(props: AssignmentPageProps, children: e.HTMLElement):
    return Layout(f"Assignments for {props.course.name}", children)


async def get_ssr_props(request: Request) -> AssignmentPageProps:
    course_id = request.path_params["course_id"]
    courses = await query("SELECT * FROM courses WHERE id = ?", [course_id], cls=Course)
    assignments = await query(
        "SELECT * FROM assignments WHERE course_id = ?",
        [course_id],
        cls=Assignment,
    )

    if not courses:
        raise HTTPException(404, "Not found")
    return AssignmentPageProps(courses[0], assignments)


def page(props: AssignmentPageProps):
    cards = []
    for assignment in props.assignments:
        cards.append(
            Card(
                assignment.name,
                e.p(children=assignment.short_description),
                LinkButton(f"/course/{props.course.id}/assignment/{assignment.id}", "Detail"),
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
