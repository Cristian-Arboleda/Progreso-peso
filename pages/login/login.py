# %%
from dash import Dash, html, dcc, callback, Input, Output, State, register_page
import json

register_page(__name__, path='/')

layout = (
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
)

@callback(
    Output(component_id='nombre_incorrecto', component_property='style'),
    Output(component_id='contrasena_incorrecto', component_property='style'),
    Output(component_id='url', component_property='pathname'),
    Input(component_id='button_enviar', component_property='n_clicks'),
    State(component_id='nombre_usuario', component_property='value'),
    State(component_id='contrasena', component_property='value'),
)

def verificacion_inicio_sesion(n_clicks, nombre_usuario, contrasena):
    if not n_clicks:
        return {'display': 'none'}, {'display': 'none'}, None
    
    with open('pages/login/credenciales.json', 'r') as file:
        credenciales = json.load(file)
    
    # Si el nombre de usuario no existe
    if nombre_usuario not in credenciales:
        print('El nombre de usuario no existe')
        return {'display': 'flex'}, {'display': 'none'}, None
    
    # Si la contrasena es incorrecta
    if contrasena != credenciales[nombre_usuario]['password']:
        return {'display': 'none'}, {'display': 'flex'}, None
    
    # 🔹 credenciales correctas
    
    # Guarda el usuario en el archivo inicio.json
    
    with open('pages/login/inicio.json', 'w') as file:
        json.dump({'sesion_iniciada_por': nombre_usuario}, file, indent=4)
    
    # Ir a la pagina de dashboard
    return {'display': 'none'}, {'display': 'none'}, '/dashboard'
# %%
