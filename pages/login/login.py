from dash import register_page, html, dcc, callback, Input, Output, State, no_update
import json
import os
from conectar_db import *

register_page(__name__, path='/login')

layout = html.Div(
    id='recuadro_inicio_sesion', 
    children=[
        html.Link(
            rel='stylesheet',
            href='assets/login.css',
        ),
        html.P('Iniciar Sesion', className='p_iniciar_sesion'),
        dcc.Input(id='nombre_usuario', type='text', placeholder='Nombre de usuario', className='input'),
        html.P('Nombre usuario incorrecto', id='nombre_usuario_incorrecto', className='p_incorrecto'),
        dcc.Input(id='password', type='password', placeholder='Password', className='input'),
        html.P('Contrasena incorrecta', id='password_incorrecta', className='p_incorrecto'),
        html.Button('Enviar', id='enviar'),
        dcc.Location(id='url'),
        dcc.Store(id='almacenamiento_datos', storage_type='session')
])

@callback(
    Output(component_id='nombre_usuario_incorrecto', component_property='style'),
    Output(component_id='password_incorrecta', component_property='style'),
    Output(component_id='url', component_property='pathname'),
    Output(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='enviar', component_property='n_clicks'),
    State(component_id='nombre_usuario', component_property='value'),
    State(component_id='password', component_property='value'),
    prevent_initial_call=True,
)

def verificacion_inicio_sesion(n_clicks, nombre_usuario, password):
    if not n_clicks:
        print('No se ha presionado el button enviar')
        return no_update, no_update, no_update, no_update
    
    # El nombre de la tabla donde se van a obtener las crdenciales
    tabla = 'credenciales'
    
    # Verificar que el usuario se encuentre registrado
    query = f"""
    SELECT usuario FROM {tabla}
    WHERE usuario = '{nombre_usuario}'
    """
    
    # Si la culsulta no arroja un resultado significa que el usuario no se encuentra registrado en la basa de datos tabla credenciales
    if not consulta_db(query=query, obtener_datos='uno'):
        print(f'El nombre de usuario {nombre_usuario} no se encuentra registrado')
        return {'display': 'flex'}, {'display': 'none'}, no_update, no_update
    
    # Verificar que la contrasena sea correcta para el usuario digitado
    query = f"""
    SELECT password FROM {tabla}
    WHERE usuario = '{nombre_usuario}'
    """
    # obtener la contrasena de la base de datos
    if not consulta_db(query=query, obtener_datos='uno')[0] == password:
        print(f'La contrasena para {nombre_usuario} es incorrecta')
        return {'display': 'none'}, {'display': 'flex'}, no_update, no_update
    
    print(f'Iniciando sesion: {nombre_usuario}')
    return  no_update, no_update, '/dashboard', {'sesion_iniciada_por': nombre_usuario}
