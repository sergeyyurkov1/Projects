from dash import html, Input, Output, State, Dash, dcc, callback  # callback_context
import dash_bootstrap_components as dbc

# import grasia_dash_components as gdc

from apps import adsb_tracker

external_scripts = ["https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"]

# --- App start ------------------------------------------------------------------------------------------
app = Dash(
    __name__,
    external_scripts=external_scripts,
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
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Links", header=True),
                        dbc.DropdownMenuItem(
                            html.A(
                                "Projects",
                                href="/",
                                style={
                                    "padding-left": "10px",
                                    "padding-right": "10px",
                                    "textDecoration": "none",
                                },
                                className="text-light",
                            )
                        ),
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

footer = html.Footer(
    [
        html.Div(
            html.P(
                "Background made with Particles.js",
                # className="text-muted",
                style={
                    "font-size": "12px",
                    "color": "white",
                    "display": "inline-block",
                },
            ),
            className="container",
        )
    ],
    className="footer bg-primary",  # bg-info, bg-primary
    style={
        # "background": "transparent",
        "position": "absolute",
        # "position": "relative",
        "bottom": "0",
        "width": "100%",
        "height": "40px",
        "z-index": "1100",
        "text-align": "right",
    },
)

app.layout = html.Div(
    [dcc.Location(id="url"), *navbar, content], id="layout"
)  # , footer


def get_card(src, title, desc, href, sc_href, sc_disabled):
    if "http" in href:
        external_link = True
        target = "_blank"
    else:
        external_link = False
        target = ""

    return dbc.Card(
        [
            dbc.CardImg(src=src, top=True),
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    html.P(
                        desc,
                        className="card-text",
                    ),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                [
                                    "Open",
                                    " ",
                                    html.I(className="bi bi-box-arrow-up-right"),
                                ],
                                color="secondary",
                                external_link=external_link,
                                target=target,
                                outline=True,
                                href=href,
                            ),
                            dbc.Button(
                                html.I(className="bi bi-github"),
                                href=sc_href,
                                target="_blank",
                                # className="text-secondary",
                                color="primary",
                                disabled=sc_disabled,
                                # style={
                                #     "textDecoration": "none",
                                # },
                            ),
                        ]
                    ),
                ],
                className="d-grid",
            ),
        ],
        style={"width": "18rem", "padding": "10px", "margin": "40px 20px 0px 20px"},
        className="bg-light ",
    )


_home = (
    html.Div(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            get_card(
                                src="assets/images/01.jpg",
                                title="ADS-B Tracker",
                                desc="Simple flight tracker and weather radar",
                                href="/adsb_tracker",
                                sc_href="/",
                                sc_disabled=True,
                            ),
                            get_card(
                                src="assets/2.png",
                                title="Vaccination Goals",
                                desc="Visualizes vaccination progress, past and future milestones",
                                href="https://sy-projects-st.herokuapp.com/?app=Vaccination+Goal+Visualizer",
                                sc_href="https://github.com/sergeyyurkov1/sy-projects-st/blob/main/apps/vaccination_goals.py",
                                sc_disabled=False,
                            ),
                        ],
                        justify="center",
                    ),
                    dbc.Row("", style={"height": "80px"}),
                ]
            ),
            footer,
        ],
        id="particles-js",
    ),
)

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
    elif pathname == "/":
        return _home, "Projects"
    return _404, ""


if __name__ == "__main__":
    app.run_server(debug=True)  # host="0.0.0.0"
