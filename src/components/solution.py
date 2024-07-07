from libsql_client import Row
import liku as e

from src.components.button import LinkButton
from src.components.collapse import Collapse
from src.db import query
from src.components.card import Card


def SubmitSolution(assignment_id: str):
    return e.form(
        props={
            "action": f"./{assignment_id}/submit",
            "method": "POST",
            "enctype": "multipart/form-data",
        },
        children=Card(
            class_="bg-neutral",
            title="Submit Solution",
            body=e.div(
                props={"class_": "flex flex-col gap-4"},
                children=[
                    e.input(
                        {
                            "type": "file",
                            "name": "file",
                            "class_": "file-input file-input-bordered w-full file-input-sm",
                            "accept": ".pdf,.py,.java,.zip",
                        }
                    ),
                    e.label(
                        props={"class_": "form-control"},
                        children=[
                            e.span(props={"class_": "label-text"}, children="Detail"),
                            e.textarea(
                                props={
                                    "name": "notes",
                                    "rows": 10,
                                    "class_": "textarea textarea-bordered",
                                    "placeholder": "Describe your solution",
                                }
                            ),
                        ],
                    ),
                ],
            ),
            actions=e.button(
                props={"type": "submit", "class_": "btn btn-info"},
                children="Submit",
            ),
        ),
    )


def SolutionCollapse(solution: Row):
    return Collapse(
        summary=str(solution["user_name"]),
        content=e.div(
            children=[
                e.p(props={"class_": "pb-2"}, children=str(solution["notes"]) or "No details provided"),
                LinkButton(href=str(solution["url"]), label="View Solution", class_="btn-sm"),
            ],
        ),
    )


async def SolutionsList(assignment_id: str):
    solutions = await query(
        """
        SELECT s.url AS url, s.notes AS notes, u.name AS user_name FROM submissions s
        JOIN users u ON s.user_id = u.npm
        WHERE assignment_id = ?
    """,
        [assignment_id],
    )

    return Card(
        class_="bg-neutral",
        title="Solutions",
        body=e.div(
            props={"class_": "flex flex-col gap-2"},
            children=[SolutionCollapse(s) for s in solutions],
        ),
    )
