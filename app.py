from dash import Dash, html
import os

app = Dash(
    __name__,
    use_pages=True,
)

server = app.server



if __name__ == "__main__":
    app.run_server(port=8050, debug=True)