from dash import register_page, html, dcc, callback, Input, Output, State
import json

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

@callback(
    Input(component_id='enviar', component_property='n_clicks'),
    Input(component_id='nombre_usuario', component_property='value')
)

def verificacion_inicio_sesion(n_clicks):
    if not n_clicks:
        print('No se ha presionado el button enviar')
        return
    
    with open('login/credenciales.json', 'r') as file:
        pass
