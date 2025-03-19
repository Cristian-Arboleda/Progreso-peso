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
                            dcc.Input(id='peso_input_agregar', type='number', value=60),
                        ]),
                        html.Button('Agregar', id='agregar_button')
                    ])
                ]),
                # ----------------------------------------------------------------------------------
                dcc.Tab(label='Eliminar', value='eliminar', children=[
                    html.Div(id = 'eliminar_tab', children=[
                        html.Label('ID'),
                        dcc.Input(id='id_eliminar')
                    ])
                ]),
            ]
        ),
        html.Div(id = 'tabla_db'),
    ])
])

# mantener actualizados los valores del input 

@callback(
    Output(component_id='id_input_agregar', component_property='value' ),
    Output(component_id='fecha_input_agregar', component_property='value'),
    Input(component_id='almacenamiento_datos',component_property='data'),
)

def actualizar_valores_inputs(almacenamiento_datos):
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
    print(f"Datos enviados a la base de datos progreso_peso_bd tabla: {tabla}")
    print("-"*100)
    return 


# Actualizar tabla
@callback(
    Output(component_id='tabla_db', component_property='children'),
    Input(component_id='agregar_button', component_property='n_clicks'),
    State(component_id='almacenamiento_datos', component_property='data'),
)

def actualizar_tabla(n_clicks, data):
    """
    Actualiza la tabla de datos para mostrar los datos mas recientes de la base de datos del usuario
    Args:
        n_clicks (int): numero de clicks en el boton agregar
        data (list): lista de datos relacionado con el incio de sesion del usuario 
    """
    # obtener usuario
    usuario = data['sesion_iniciada_por']
    
    #crear conexion con la base de datos
    conn = conectar_db()
    
    # Crear consulta para obtener los datos de la base datos
    query = f"SELECT * FROM progreso_peso_{usuario} ORDER BY id DESC" 
    
    # convertir a pandas
    datos_usuario_peso = pd.read_sql(query, conn)
    
    #cerrar conexion con la base de datos
    conn.close()
    
    # Crear la tabla que muestrar los registros del peso del usuario
    tabla = dash_table.DataTable(
        data=datos_usuario_peso.to_dict('records'), # convertir a formato permitido por dash_table
        columns=[{"name": nombre_col.title(), "id": nombre_col,} for nombre_col in datos_usuario_peso.columns],
        page_size= 6,
        cell_selectable=False,
        style_header={
            "color": "white", "background": "black",
            "font-size": "25px", "font-weight": "bold", "padding": "13px",
            },
        style_cell={
            'padding': '10px', 'text-align': 'center',
            'font-size': '20px',
            'border': 'none'
        },
        style_data_conditional=[
            # Color de las filas pares (0, 2, 4...)
            {
                "if": {"row_index": "even"},
                "background": "#f9f9f9",
            },
            # Color de las filas impares (1, 3, 5...)
            {
                "if": {"row_index": "odd"},
                "background": "#e9e9e9",
            },
        ],
    )
    return tabla
    