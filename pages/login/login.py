# %%
from dash import Dash, html, dcc, callback, Input, Output, State, register_page, no_update
import json
import time

register_page(__name__, path='/')

layout = html.Div([
    dcc.Store(id='almacenamiento_datos', data={}, storage_type='session'),
    html.Div(
        children=[
            dcc.Location(id='url'),
            html.Div(
                className='recuadro-inicio-de-sesion',
                id='recuadro-inicio-de-sesion',
                children=[
                    html.P(
                        'Iniciar sesion',
                        style={'text-align': 'center', 'font-size': '25px', 'margin': '20px'}
                    ),
                    dcc.Input(id='nombre_usuario', className='input-inicio-sesion', placeholder='Nombre de usuario', type='text'),
                    html.P('Nombre de usuario incorecto', id='nombre_incorrecto', className='incorrecto'),
                    dcc.Input(id='contrasena', className='input-inicio-sesion', placeholder='Password', type='password'),
                    html.P('Contrasena incorrecta', id='contrasena_incorrecto', className='incorrecto'),
                    html.Button('Enviar', id='button_enviar',
                    )
                ]
            )
        ]
    )
])

@callback(
    Output(component_id='nombre_incorrecto', component_property='style'),
    Output(component_id='contrasena_incorrecto', component_property='style'),
    Output(component_id='url', component_property='pathname'),
    Output(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='button_enviar', component_property='n_clicks'),
    State(component_id='nombre_usuario', component_property='value'),
    State(component_id='contrasena', component_property='value'),
    prevent_initial_call=True,
)

def verificacion_inicio_sesion(n_clicks, nombre_usuario, contrasena):
    if not n_clicks:
        return {'display': 'none'}, {'display': 'none'}, None, no_update
    
    with open('pages/login/credenciales.json', 'r') as file:
        credenciales = json.load(file)
    
    # Si el nombre de usuario no existe
    if nombre_usuario not in credenciales:
        print('El nombre de usuario no existe')
        return {'display': 'flex'}, {'display': 'none'}, None, no_update
    
    # Si la contrasena es incorrecta
    if contrasena != credenciales[nombre_usuario]['password']:
        return {'display': 'none'}, {'display': 'flex'}, None, no_update
    
    # 🔹 credenciales correctas
    
    # Ir a la pagina de dashboard
    return {'display': 'none'}, {'display': 'none'}, f'/practica', {'sesion_iniciada_por': nombre_usuario}
# %%
