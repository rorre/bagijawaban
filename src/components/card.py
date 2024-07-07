import liku as e


def Card(
    title: e.HTMLNode | None = None,
    body: e.HTMLNode | None = None,
    actions: e.HTMLNode | None = None,
    class_: str = "",
    body_class_: str = "",
    actions_class_: str = "",
):
    return e.div(
        props={"class_": "card " + class_},
        children=e.div(
            props={"class_": "card-body " + body_class_},
            children=[
                e.strong(props={"class_": "card-title"}, children=title),
                e.Fragment(children=body),
                e.div(
                    props={"class_": "card-actions justify-end " + actions_class_},
                    children=actions,
                ),
            ],
        ),
    )
