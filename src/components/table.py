import liku as e


def Table(data: list[list[object]], header: list[str] | None = None):
    return e.table(
        props={"class_": "table"},
        children=[
            e.thead(children=[e.th(children=h) for h in header]) if header else None,
            e.tbody(
                children=[
                    e.tr(children=[e.td(children=d if isinstance(d, e.HTMLElement) else str(d)) for d in row])
                    for row in data
                ]
            ),
        ],
    )
