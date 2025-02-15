# %%
from dash import Dash, html, dcc, callback, Input, Output, State
import json

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=['assets/login.css'])

server = app.server


if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
# %%
