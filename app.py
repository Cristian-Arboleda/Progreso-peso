from dash import Dash

app = Dash(__name__)

app.server

app.run_server(port=8050, debug=True)