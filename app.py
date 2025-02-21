from dash import Dash, html, dcc, callback, Input, Output, State

app = Dash(__name__)

app.server

app.run_server(port=8050, debug=True)