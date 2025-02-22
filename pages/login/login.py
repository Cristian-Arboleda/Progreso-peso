from dash import register_page, html, dcc, callback, Input, Output, State, no_update
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
    html.Button('Enviar', id='enviar'),
    dcc.Location(id='url')
])

@callback(
    Output(component_id='nombre_usuario_incorrecto', component_property='style'),
    Output(component_id='password_incorrecta', component_property='style'),
    Output(component_id='url', component_property='pathname'),
    Input(component_id='enviar', component_property='n_clicks'),
    State(component_id='nombre_usuario', component_property='value'),
    State(component_id='password', component_property='value'),
)

def verificacion_inicio_sesion(n_clicks, nombre_usuario, password):
    if not n_clicks:
        print('No se ha presionado el button enviar')
        return
    
    with open('pages/login/credenciales.json', 'r') as file:
        credenciales = json.load(file)
    
    if nombre_usuario not in credenciales:
        print('El nombre de usuario no se encuentra')
        return {'display': 'flex'}, {'display': 'none'}, no_update
    
    if password != credenciales[nombre_usuario]['password']:
        print(f'La contrasena para {nombre_usuario} es incorrecta')
        return {'display': 'none'}, {'display': 'flex'}, no_update
    
    # Credenciales correctas
    
    return  no_update, no_update, '/dashboard'
