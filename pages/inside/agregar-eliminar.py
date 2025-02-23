from dash import register_page, html

register_page(__name__, path='/agregar-eliminar')

layout = html.Main([
    html.Link(
        rel='stylesheet',
        href='assets/agregar-eliminar.css',
    ),
    html.Div(className='agregar', children=[
        html.P('ID:')
    ])
])