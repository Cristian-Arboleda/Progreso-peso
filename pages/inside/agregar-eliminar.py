from dash import register_page, html, dcc, callback, Input, Output, State, dash_table, no_update
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
        dcc.Tabs(
            id='agregar-eliminar_tab', value='agregar', children=[
                # --------------------------------------------------------------------------------
                dcc.Tab(label='Agregar', value='agregar', children=[
                    html.Div(id='agregar_tab', children=[
                        html.Div(className='agregar_div', children=[
                            html.Label('ID', htmlFor='id_agregar'),
                            dcc.Input(id='id_input_agregar', type='number',),
                        ]),
                        html.Div(className='agregar_div', children=[
                            html.Label('Fecha', htmlFor='fecha_agregar'),
                            dcc.Input(id='fecha_input_agregar', type='text'),
                        ]),
                        html.Div(className='agregar_div', children=[
                            html.Label('Ciclo', htmlFor='ciclo_agregar'),
                            dcc.Dropdown(
                                id='ciclo_dropdown_agregar',
                                options=[
                                    {'label': 'Diurno', 'value': 'diurno'},
                                    {'label': 'Nocturno', 'value': 'nocturno'}
                                ],
                                value='diurno',
                                clearable=False,
                                searchable=False,
                                style={'width': '150px', 'font-size': '20px', 'cursor': 'pointer'}
                            ),
                        ]),
                        html.Div(className='agregar_div', children=[
                            html.Label('Peso'),
                            dcc.Input(id='peso_input_agregar', type='number'),
                        ]),
                        html.Button('Agregar', id='agregar_button')
                    ])
                ]),
                # ----------------------------------------------------------------------------------
                dcc.Tab(label='Eliminar', value='eliminar', children=[
                    html.Div('eliminar')
                ]),
                html.Div(id='mensaje_enviado')
            ]
        ),
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


# mantener los valores del inpur actualizados

@callback(
    Output(component_id='id_input_agregar', component_property='value' ),
    Output(component_id='fecha_input_agregar', component_property='value'),
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



# Enviar valores de los inputs a database.json al presionar el boton enviar

@callback(
    Input(component_id='agregar_button', component_property='n_clicks'),
    State(component_id='id_input_agregar', component_property='value'),
    State(component_id='fecha_input_agregar', component_property='value'),
    State(component_id='ciclo_dropdown_agregar', component_property='value'),
    State(component_id='peso_input_agregar', component_property='value'),
    State(component_id='almacenamiento_datos', component_property='data'),
)

def enviar_datos(n_clicks, id, fecha, ciclo, peso, data):
    if not n_clicks:
        print(f'Clicks: {n_clicks}')
        return 
    
    # cargar datos
    with open(database_path, 'r') as file:
        database = json.load(file)
    
    print(database)
    
    # Obtener usuario que inicio sesion
    usuario = data['sesion_iniciada_por']
    
    # Si el id no exite inicilizarlo, esto evita que borre ciclos que ya se hayan creado
    
    if not str(id) in database[usuario]:
        database[usuario][str(id)] = {}
    
    # actualizar fecha
    database[usuario][str(id)]['fecha'] = fecha
    
    # actualizar ciclo
    database[usuario][str(id)][ciclo] = peso
    
    # guardar base de datos con los datos insertados
    with open(database_path, 'w') as file:
        json.dump(database, file, indent=4)
    
    print(f'Se guardo: {database[usuario][str(id)]}')
    return 
    
    
