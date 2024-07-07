import liku as e
from dataclasses import dataclass
from src.components.card import Card
from src.components.button import LinkButton
from src.components.table import Table
from src.models import Course
from src.db import query
from src.components.layout import Layout

from starlette.requests import Request
from libsql_client import ResultSet


@dataclass
class CourseProps:
    courses: ResultSet


layout = Layout


async def get_ssr_props(request: Request) -> CourseProps:
    courses = await query(
        """
        SELECT c.id AS id, c.name AS name, COUNT(a.id) AS total_assignments
        FROM courses c LEFT JOIN assignments a ON a.course_id = c.id
        GROUP BY c.id
        """
    )
    return CourseProps(courses)


def page(props: CourseProps) -> e.HTMLElement:
    return e.div(
        props={"class_": "flex flex-col gap-4 py-8"},
        children=[
            e.h1(
                props={
                    "class_": "text-3xl font-bold",
                },
                children="Courses",
            ),
            e.div(
                props={"class_": "grid grid-cols-1 md:grid-cols-2 gap-4"},
                children=[
                    Card(
                        str(course["name"]),
                        e.p(children=f"Assignments: {course["total_assignments"]}"),
                        LinkButton(f"/course/{course["id"]}/assignment", "Assignments"),
                        class_="bg-neutral",
                    )
                    for course in props.courses
                ],
            ),
        ],
    )
