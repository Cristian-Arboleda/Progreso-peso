from dash import Dash

app = Dash(__name__,use_pages=True)

app.server

app.run_server(port=8050, debug=True)