from dash import Dash, html

app = Dash(
    __name__,
    use_pages=True,
)

app.server

app.layout =html.Div([
    
])

app.run_server(port=8050, debug=True)