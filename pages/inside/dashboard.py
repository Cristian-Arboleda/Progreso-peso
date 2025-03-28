from dash import register_page, html, dcc, callback, Input, Output
from conectar_db import *

register_page(__name__, path='/dashboard')

pesos_id = ['peso_inicial', 'peso_actual', 'peso_perdido', 'peso_mayor', 'peso_menor', 'peso_perdido_en_promedio']

layout = html.Main(children=[
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    html.Link(rel='stylesheet', href='assets/dashboard.css'),
    # ------------------------------------------------------------------
    html.Div(className= 'div_contenedor_opciones_principales', children=[
        dcc.Dropdown(
            id = 'dropdown_years',
            clearable=False,
            searchable=False,
            multi=True,
            style={'width': '300px'},
            ),
        dcc.Dropdown(
            id = 'dropdown_months',
            clearable=False,
            searchable=False,
            multi=True,
            style={'width': '500px'},
        ),
    ]),
    html.Div(className='div_contenedor_peso', children=[
        *[html.Div(className= 'divs_peso',children=[
        html.P(peso_id.replace("_", " ").title(), className='p_peso_texto'),
        html.Div(id=peso_id)
        ])
        for peso_id in pesos_id]
    ]),
    
])

@callback(
    Output(component_id='dropdown_years', component_property='options'),
    Output(component_id='dropdown_years', component_property='value'),
    Input(component_id='almacenamiento_datos', component_property='data'),
)
def actualizar_dropdown_years(data):
    usuario = data['sesion_iniciada_por']
    
    query = f"""
    SELECT DISTINCT EXTRACT(YEAR FROM fecha) AS year
    FROM progreso_peso_{usuario}
    ORDER BY year
    """
    years_db = consulta_db(query=query, obtener_datos='todos')
    
    if not years_db:
        resultado = [{'label': 'No hay registros'}]
        value = 'null'
        return resultado, value  
    
    years_list = [year[0] for year in years_db]
    years_list.append('Todos')
    
    resultado = [
        {'label': year, 'value': year}
        for year in years_list
    ]
    
    # Obtener el valor que se va a mostrar al cargar la pagina en el dropdown years
    value = years_list[-2]
    
    return resultado, value

@callback(
    Output(component_id='dropdown_months', component_property='options'),
    Output(component_id='dropdown_months', component_property='value'),
    Input(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='dropdown_years', component_property='value'), # el year es el indice donde se van a obntener los meses
)
def actualizar_dropdown_months(data, years_list):
    usuario = data['sesion_iniciada_por']
    
    if not years_list:
        return [{'label': 'Seleccione un año', 'value': ''}], ''
    
    # Si los years no estan en una lista, convertirla en una lista
    if not isinstance(years_list, list):
        years_list = [years_list]
    
    if 'Todos' in years_list:
        query = f"""
        SELECT DISTINCT EXTRACT(MONTH FROM fecha) AS mes
        FROM progreso_peso_{usuario}
        ORDER BY mes
        """
    else:
        if len(years_list) == 1:
            query = f"""
                SELECT DISTINCT EXTRACT(MONTH FROM fecha) AS mes
                FROM progreso_peso_{usuario}
                WHERE EXTRACT(YEAR FROM fecha) IN ({years_list[0]})
                ORDER BY mes
            """
        else:
            query = f"""
                SELECT DISTINCT EXTRACT(MONTH FROM fecha) AS mes
                FROM progreso_peso_{usuario}
                WHERE EXTRACT(YEAR FROM fecha) IN {tuple(years_list)}
                ORDER BY mes
            """
    
    # realizar consulta a la base de datos
    months_db = consulta_db(query=query, obtener_datos='todos')
    
    # Convertir months_db en una lista
    months_index_list = [str(month_index[0]) for month_index in months_db]
    months = {
        '1': 'enero',
        '2': 'febrero', 
        '3': 'marzo', 
        '4': 'abril', 
        '5': 'mayo', 
        '6': 'Junio', 
        '7': 'julio', 
        '8': 'agosto',
        '9': 'septiembre',
        '10': 'octubre',
        '11': 'noviembre',
        '12': 'diciembre'
    }
    months_por_years= [months[month_index] for month_index in months_index_list]
    months_list = [{'label': month.title(), 'value': index_month} for month, index_month in zip(months_por_years, months_index_list)]
    
    return months_list, months_index_list[-1]


@callback(
    [Output(component_id = ids, component_property = 'children') for ids in pesos_id],
    Input(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='dropdown_years', component_property='value'),
    Input(component_id='dropdown_months', component_property='value'),
)
def actualizar_los_datos_del_peso(data, years, months):
    usuario = data['sesion_iniciada_por']
    
    datos_peso = {dato: 'Sin valor' for dato in pesos_id}
    
    # verificar que el los meses y los years no esten vacios
    if not years or not months:
        return [dato for dato in datos_peso.values()]
    
    #
    if not isinstance(years, list):
        years = [years]
    if not isinstance(months, list):
        months = [months]
    
    # Obtener de la base de datos el peso inicial en base al years y el months seleccionados
    query = f"""
    SELECT diurno FROM progreso_peso_{usuario}
    WHERE EXTRACT(YEAR FROM fecha) = {min(years)}  -- Año específico
    AND EXTRACT(MONTH FROM fecha) = {min(months)}    -- Mes específico
    ORDER BY fecha ASC  -- Ordenar por fecha ascendente (más antigua primero)
    LIMIT 1;
    """
    valor = consulta_db(query=query, obtener_datos='uno')
    print('peso inicial', valor)
    
    # 
    if valor:
        datos_peso['peso_inicial'] = valor[0]
    
    # Obtener de la base de datos el peso actual
    query="""
    
    """
    
    return [dato_peso for dato_peso in datos_peso.values()]
