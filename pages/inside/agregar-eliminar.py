from dash import register_page, html, dcc, callback, Input, Output, State, dash_table
import os
import json
from datetime import date


register_page(__name__, path='/agregar-eliminar')

layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='assets/agregar-eliminar.css',
    ),
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    
    # ------------------------------------------------------
    
    html.Div(id='titulo_nombre_usuario'),
    html.Main([
        html.H1('Agregar'),
        html.Div(id='agregar', children=[
            html.Label('ID:', htmlFor='id_agregar'),
            dcc.Input(id='id_agregar', type='number',),
            html.Label('Fecha:', htmlFor='fecha_agregar'),
            dcc.Input(id='fecha_agregar', type='text'),
            html.Label('Ciclo:', htmlFor='ciclo_agregar'),
            dcc.Dropdown(
                id='ciclo_agregar',
                options=[
                    {'label': 'Diurno', 'value': 'diurno'},
                    {'label': 'Nocturno', 'value': 'nocturno'}
                ],
                value='diurno',
                clearable=False,
                style={'width': '150px', 'font-size': '20px'}
            ),
            html.Label('Peso:'),
            dcc.Input(id='peso_agregar', type='number'),
            html.Button('Agregar', id='agregar_button')
        ]),
        html.Hr(),
        html.H1('Eliminar'),
        html.Div(id='eliminar', children=[
            
        ]),
        dash_table.DataTable(
            id='database_table',
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "Nombre", "id": "nombre"},
                {"name": "Edad", "id": "edad"}
            ],
            data=[
                {"id": 1, "nombre": "Carlos", "edad": 25},
            ]
        )
    ])
])


# obtener el path de database.json

current_dir = os.path.dirname(__file__)  
database_path = os.path.join(current_dir, "database.json")


# nombre del usuario 

@callback(
    Output(component_id='titulo_nombre_usuario', component_property='children'),
    Input(component_id='almacenamiento_datos', component_property='data'),
)

def update_nombre_usuario(almacenamiento_datos):
    if almacenamiento_datos is None:
        print('No se encuentra el nombre del usuario que inicio sesion')
        return 'Nada'
    print('Estableciendo el nombre de usuario')
    nombre_usuario = almacenamiento_datos['sesion_iniciada_por']
    return nombre_usuario


# actualizar valores de input

@callback(
    Output(component_id='id_agregar', component_property='value' ),
    Output(component_id='fecha_agregar', component_property='value'),
    Input(component_id='almacenamiento_datos',component_property='data'),
)

def update_valores_inputs(almacenamiento_datos):
    print('Actualizando los valores de los inputs de agregar')
    
    # Obtener el nombre de quien haya iniciado sesion
    nombre_usuario = almacenamiento_datos['sesion_iniciada_por']
    
    # Obtener la base de datos
    
    with open(database_path, 'r') as file:
        database = json.load(file)
    
    
    # Obtener siguiente ID
    siguiente_id = int(list(database[nombre_usuario].keys())[-1]) + 1 
    
    # Obtener la fecha actual
    
    fecha_actual = date.today()
    
    return siguiente_id, fecha_actual




