from dash import Dash, html, dcc, callback, Input, Output, State, register_page

register_page(__name__, path='/dashboard')

layout = (
    html.H1('Bienvenido a tu dash board')
)