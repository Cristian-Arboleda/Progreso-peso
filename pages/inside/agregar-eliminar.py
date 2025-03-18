from dash import register_page, html, dcc, callback, Input, Output, State, dash_table, no_update
from datetime import date
from conectar_db import *


register_page(__name__, path='/agregar-eliminar')

layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='assets/agregar-eliminar.css',
    ),
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    
    # ------------------------------------------------------
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
            ]
        ),
        dash_table.DataTable(
            id='database_table',
            page_size=7,
            style_header={
                'font-size': '25px',
            },
            style_cell={
                'font-size': '20px',
                'padding': '10px',
            },
            cell_selectable=False
        ),
    ])
])

# mantener actualizados los valores del input 

@callback(
    Output(component_id='id_input_agregar', component_property='value' ),
    Output(component_id='fecha_input_agregar', component_property='value'),
    Input(component_id='almacenamiento_datos',component_property='data'),
)

def update_valores_inputs(almacenamiento_datos):
    print('Actualizando los valores de los inputs de agregar')
    
    # Obtener el nombre de quien haya iniciado sesion
    nombre_usuario = almacenamiento_datos['sesion_iniciada_por']
    
    # Obtener la tabla del usuario
    tabla = f'progreso_peso_{nombre_usuario}'
    
    # Crear el siguiente ID
    query = f'SELECT MAX(id) FROM {tabla}'
    ultimo_id = consulta_db(query, obtener_datos='uno')[0]
    if not ultimo_id:
        # Si no hay datos en la columna id
        siguiente_id = 1
    else:
        siguiente_id = ultimo_id + 1
    
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
    
    print(f'Datos obtenidos: {id}, {fecha}, {ciclo}, {peso}, {data}')
    
    # Es necesario que haya un id
    if not id:
        print('El id esta vacio')
        return
    
    # Obtener usuario que inicio sesion
    usuario = data['sesion_iniciada_por']
    tabla = f"progreso_peso_{usuario}"
    
    # Verificar que el id exista en la base de datos del usuario
    query = F"SELECT EXISTS (SELECT 1 FROM {tabla} WHERE id = {id})"
    id_existe = consulta_db(query, obtener_datos = 'uno')[0]
    print(f'id {id} existe: {id_existe}')
    if not id_existe:
        # Si no exite el id Crear el id
        query = f"INSERT INTO {tabla} (id) VALUES ({id})"
        consulta_db(query)
    
    # Insertar los datos en el id correspondiente atraves de la actualizacion de datos del id
    query = f"""
        UPDATE {tabla}
        SET fecha = '{fecha}', {ciclo} = {peso}
        WHERE id = {id}
    """
    consulta_db(query)
    print(f"Datos enviados a la tabla: {tabla}")
    print("-"*100)


# Actualizar tabla
@callback(
    Output(component_id='database_table', component_property='data'),
    Input(component_id='agregar_button', component_property='n_clicks'),
    Input(component_id='almacenamiento_datos', component_property='data')
)

def actualizar_tabla(n_cliks, data):
    # obtener usuario
    usuario = data['sesion_iniciada_por']
    
    # obtener los datos del progreso del usuario
    query = f'SELECT * FROM progreso_peso_{usuario}'
    conn = conectar_db()
    # convertir a pandas
    datos_usuario_peso = pd.read_sql(query, conn).to_dict('records')
    print(datos_usuario_peso)
    conn.close()
    
    return datos_usuario_peso
    