from dash import register_page, html

register_page(__name__)

layout = html.Div(children=[
    html.P('Bienvenido')
])