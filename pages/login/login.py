from dash import register_page, html, dcc

register_page(__name__, path='/')

layout = html.Div(className='recuadro_inicio_sesion', children=[
    html.P('Iniciar Sesion'),
    dcc.Input(id='nombre_usuario', type='text', placeholder='Nombre de usuario', className='input'),
    dcc.Input(id='password', type='password', placeholder='Password', className='input'),
    html.Button('Enviar', id='enviar')
])