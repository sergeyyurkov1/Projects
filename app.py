from dash import html, Input, Output, State, Dash, dcc, callback  # callback_context
import dash_bootstrap_components as dbc

from apps import adsb_tracker

# --- App start ------------------------------------------------------------------------------------------
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
        dbc.icons.BOOTSTRAP,
    ],
    update_title=None,
    title="Apps | Sergey Yurkov",
    # prevent_initial_callbacks=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no",
        }
    ],
    suppress_callback_exceptions=True,
)
server = app.server

LOGO = "assets/0.png"

navbar = (
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=LOGO, height="35px")),
                            dbc.Col(dbc.NavbarBrand("", className="ms-2", id="nvb")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="#",
                    style={"textDecoration": "none"},
                ),
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Links", header=True),
                        dbc.DropdownMenuItem(
                            html.A(
                                "Blog",
                                href="https://sergeyyurkov1.github.io/blog/",
                                style={
                                    "padding-left": "10px",
                                    "padding-right": "10px",
                                    "textDecoration": "none",
                                },
                                className="text-light",
                                target="_blank",
                            )
                        ),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Projects", header=True),
                        dbc.DropdownMenuItem(
                            dbc.NavItem(
                                [
                                    dcc.Link(
                                        "ADS-B Tracker",
                                        href="/adsb_tracker",
                                        className="text-light",
                                        style={
                                            "padding-left": "10px",
                                            "padding-right": "10px",
                                            "textDecoration": "none",
                                        },
                                    ),
                                    html.A(
                                        html.I(className="bi bi-github"),
                                        href="/",
                                        target="_blank",
                                        className="text-light",
                                        style={
                                            "textDecoration": "none",
                                        },
                                    ),
                                ],
                            ),
                            style={"display": "inline !important"},
                        ),
                        dbc.DropdownMenuItem(
                            [
                                html.A(
                                    "Vaccination Goals",
                                    href="https://sy-projects-st.herokuapp.com/?app=Vaccination+Goal+Visualizer",
                                    className="text-light",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "textDecoration": "none",
                                    },
                                    target="_blank",
                                ),
                                html.A(
                                    html.I(className="bi bi-github"),
                                    href="/",
                                    target="_blank",
                                    className="text-light",
                                    style={
                                        "textDecoration": "none",
                                    },
                                ),
                            ],
                        ),
                        dbc.DropdownMenuItem("Other", header=True),
                        dbc.DropdownMenuItem(
                            [
                                html.A(
                                    "freeCodeCamp Projects",
                                    href="https://www.freecodecamp.org/sergeyyurkov",
                                    className="text-light",
                                    target="_blank",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "textDecoration": "none",
                                    },
                                ),
                            ]
                        ),
                        dbc.DropdownMenuItem(
                            [
                                html.A(
                                    "Bubble Pop!",
                                    href="https://sy-projects-st.herokuapp.com/?app=Bubble+Pop%21",
                                    className="text-light",
                                    target="_blank",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "textDecoration": "none",
                                    },
                                ),
                                html.A(
                                    html.I(className="bi bi-github"),
                                    href="/",
                                    target="_blank",
                                    className="text-light",
                                    style={
                                        "textDecoration": "none",
                                    },
                                ),
                            ]
                        ),
                        dbc.DropdownMenuItem(
                            [
                                html.A(
                                    "Blobby",
                                    href="https://sy-projects-st.herokuapp.com/?app=Home",
                                    className="text-light",
                                    target="_blank",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "textDecoration": "none",
                                    },
                                ),
                            ]
                        ),
                    ],
                    label="Navigation",
                    menu_variant="dark",
                    align_end=True,
                    # id="ddm",
                    color="primary",
                    toggle_style={
                        "textTransform": "uppercase",
                        "background": "transparent",
                        "border": "none",
                        "color": "white",
                    },
                ),
            ]
        ),
        color="dark",
        dark=True,
        style={"border-bottom": "1px solid #0d6efd"},
    ),
)

content = html.Div(id="content")

# footer = html.Footer(
#     [html.Div("", className="container")],
#     className="footer bg-primary",  # bg-info
#     style={
#         "position": "absolute",
#         "bottom": "0",
#         "width": "100%",
#         "height": "1px",
#         "z-index": "1100",
#     },
# )

app.layout = html.Div([dcc.Location(id="url"), *navbar, content])  # , footer

_404 = html.Div(
    dbc.Container(
        [
            html.H1("404 :(", className="display-3"),
            html.P(
                "Content not found",
                className="lead",
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light",
)


@callback(
    Output("content", "children"),
    Output("nvb", "children"),
    Input("url", "pathname"),
)
def render_page_content(pathname):
    if pathname == "/adsb_tracker":
        return adsb_tracker.layout, adsb_tracker.TITLE
    return _404, ""


if __name__ == "__main__":
    app.run_server(debug=True)  # host="0.0.0.0"
