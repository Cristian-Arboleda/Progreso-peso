from dash import register_page, html, dcc

register_page(__name__, path='/')

layut = html.Div(className='recuadro_inicio_sesion', children=[
    html.P('Iniciar Sesion'),
    dcc.Input(id='nombre_usuario', type='text', placeholder='Nombre de usuario')
])