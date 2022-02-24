import dash_leaflet as dl
import dash_leaflet.express as dlx
import json
from dash import html, Input, Output, Dash, dcc
import requests
from pprint import pprint
from dash_extensions.javascript import assign
import dash_bootstrap_components as dbc

def get_states(bounds):
    bounds_ = eval(json.dumps(bounds))
    
    lamin = bounds_[0][0]
    lomin = bounds_[0][1]
    lamax = bounds_[1][0]
    lomax = bounds_[1][1]
 
    url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"

    response = requests.get(url)

    states = response.json()["states"]

    features = []

    for i in states:
        features.append({
            "lon": i[5],
            "lat":  i[6],
            "true_track": i[10],
            "icao24": i[0],
            "callsign": i[1][:-2],
            "origin_country": i[2],
            "time_position": i[3],
            "last_contact": i[4],
            "baro_altitude": i[7],
            "on_ground": i[8],
            "velocity": i[9],
            "vertical_rate": i[11],
            "sensors": i[12],
            "geo_altitude": i[13],
            "squawk": i[14],
            "spi": i[15],
            "position_source": i[16],
        })

    return features

def get_flight_status(callsign: str) -> dict:
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    url = f"https://aerodatabox.p.rapidapi.com/flights/icao24/{callsign}/{today}"

    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': "c22bc56ab3msha6d5cd5860a018bp1416c6jsn25de702cffcb"
    }

    response = requests.request("GET", url, headers=headers)

    return json.loads(response.text)[0]

def get_image_url(aircraft_model: str) -> str:
    url = "https://bing-image-search1.p.rapidapi.com/images/search"

    params = {"q": aircraft_model}

    headers = {
        'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
        'x-rapidapi-key': "c22bc56ab3msha6d5cd5860a018bp1416c6jsn25de702cffcb"
        }

    response = requests.request("GET", url, headers=headers, params=params)

    return json.loads(response.text)["value"][0]["thumbnailUrl"]


# JavaScript
point_to_layer = assign("""
    function(feature, latlng, context) {
        var marker_ = L.icon({
            iconUrl: "https://dash-leaflet.herokuapp.com/assets/icon_plane.png",
        });
        var true_track = feature.properties.true_track;
        return L.marker(latlng, { icon: marker_, rotationAngle: true_track });
    }
""")

cluster_to_layer = assign("""
    function(feature, latlng, context) {
        const count = feature.properties.point_count;
        const size =
            count <= 5 ? 'small' :
            count > 5 && count < 10 ? 'medium' : 'large';
        const icon = L.divIcon({
            html: `<div><span>${ feature.properties.point_count_abbreviated }</span></div>`,
            className: `marker-cluster marker-cluster-${ size }`,
            iconSize: L.point(40, 40)
        });

        return L.marker(latlng, { icon });
    }
""")


app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
    }]
)

PLOTLY_LOGO = "https://openskynetwork.github.io/opensky-api/_static/radar_small.png"

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("ADS-B Tracker", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
        ]),
        color="dark",
        dark=True,
    ),
    dl.Map(
        children=[dl.TileLayer(),
            dl.GeoJSON(id="data",
                options=dict(pointToLayer=point_to_layer),
                cluster=True,
                zoomToBoundsOnClick=True,
                clusterToLayer=cluster_to_layer,
                # children=[dl.Tooltip(id="tooltip")]
            ),
        ],
        style={"width": "100%", "height": "100vh"},
        id="map"
    ), # 100vw, 100vh, 500px
    dcc.Interval(
        id="interval-component",
        interval=10*1000, # in milliseconds
        n_intervals=0
    ),
    dbc.Modal(
        id="modal-centered",
        centered=True,
        is_open=False,
    ),
])

@app.callback(
    Output("modal-centered", "children"),
    Output("modal-centered", "is_open"),
    [Input("data", "click_feature")], # hover_feature
)
def update_tooltip(feature):
    if feature is None:
        return None

    flight_status = get_flight_status(feature["properties"]["icao24"])
    aircraft_model = flight_status["aircraft"]["model"]
    departure_airport = flight_status["departure"]["airport"]["municipalityName"]
    arrival_airport = flight_status["arrival"]["airport"]["municipalityName"]
    airline_name = flight_status["airline"]["name"]

    image_url = get_image_url(f"{airline_name} {aircraft_model}")

    return ([
        dbc.ModalHeader(dbc.ModalTitle(f'{feature["properties"]["callsign"]} {departure_airport} -> {arrival_airport}'), close_button=True),
        dbc.ModalBody(
            dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.P(f'''Heading: {hover_feature["properties"]["true_track"]}'''),
                            html.P(f'''Grounded: {hover_feature["properties"]["on_ground"]}'''),
                            html.P(f'''Speed: {hover_feature["properties"]["velocity"]} m/s'''),
                            html.P(f'''Vertical speed: {hover_feature["properties"]["vertical_rate"]} m/s'''),
                            html.P(f'''Altitude: {hover_feature["properties"]["geo_altitude"]} meters'''),
                            # html.P(f'''Squawk code: {hover_feature["properties"]["squawk"]}''')
                        ], style={"whiteSpace": "pre-wrap"}),
                    ),
                    dbc.Col([
                        dbc.Row(html.P(f"{airline_name} {aircraft_model}")),
                        dbc.Row(html.Img(src=image_url,
                            # height="200px"
                        )),
                    ]),
                ], # className="g-0",
            ),
        )
    ], True)

@app.callback(
    Output("data", "data"),
    Input("map", "bounds"),
    Input("interval-component", "n_intervals"),
)
def log_bounds(bounds, n_intervals):
    states = get_states(bounds)
    geojson = dlx.dicts_to_geojson([{**state} for state in states]) # , **dict(tooltip = state["callsign"])
    return geojson

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
