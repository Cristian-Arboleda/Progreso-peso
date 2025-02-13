# %%
from dash import Dash, html, dcc, callback, Input, Output, State, dash_table
import json

app = Dash(__name__, external_stylesheets=['assets/style.css'])
server = app.server

app.layout = (
    html.Div(
        children=[
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
    Input(component_id='button_enviar', component_property='n_clicks'),
    State(component_id='nombre_usuario', component_property='value'),
    State(component_id='contrasena', component_property='value'),
)

def verificacion_inicio_sesion(n_clicks, nombre_usuario, contrasena):
    if not n_clicks:
        return {'display': 'none'}, {'display': 'none'}
    
    with open('credenciales.json', 'r') as file:
        credenciales = json.load(file)
    
    # Si el nombre de usuario no existe
    if nombre_usuario not in credenciales:
        print('El nombre de usuario no existe')
        return {'display': 'flex'}, {'display': 'none'}
    
    # Si la contrasena es incorrecta
    if contrasena != credenciales[nombre_usuario]['password']:
        return {'display': 'none'}, {'display': 'flex'}
    
    # si el usuario y la contrasena son correctas
    return {'display': 'none'}, {'display': 'none'}


if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
# %%
