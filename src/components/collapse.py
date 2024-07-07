import liku as e


def Collapse(summary: e.HTMLNode, content: e.HTMLNode):
    return e.details(
        props={"class_": "collapse bg-base-200"},
        children=[
            e.summary(
                props={"class_": "collapse-title text-xl font-medium"},
                children=summary,
            ),
            e.div(
                props={"class_": "collapse-content"},
                children=content,
            ),
        ],
    )
