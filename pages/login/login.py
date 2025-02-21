from dash import register_page, html, dcc, callback, Input, Output, State

register_page(__name__, path='/')

layout = html.Div(
    id='recuadro_inicio_sesion', 
    children=[
    html.P('Iniciar Sesion', className='p_iniciar_sesion'),
    dcc.Input(id='nombre_usuario', type='text', placeholder='Nombre de usuario', className='input'),
    html.P('Nombre usuario incorrecto', id='nombre_usuario_incorrecto', className='p_incorrecto'),
    dcc.Input(id='password', type='password', placeholder='Password', className='input'),
    html.P('Contrasena incorrecta', id='password_incorrecta', className='p_incorrecto'),
    html.Button('Enviar', id='enviar')
])

