from dash import register_page, html, dcc, callback, Input, Output
from conectar_db import *

register_page(__name__, path='/dashboard')

pesos_id = ['peso_inicial', 'peso_actual', 'peso_perdido', 'mayor_peso', 'menor_peso']

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
        *[html.Div(className= 'divs_item_peso',children=[
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
    
    print(f'Años seleccionados: {years_list} {type(years_list)}')
    
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
    print(months_db)
    
    # Convertir months_db en una lista
    months_index_list = [str(month_index[0]) for month_index in months_db]
    print(months_index_list)
    
    months = {'1': 'enero', '2': 'febrero', '3': 'marzo', '4': 'abril', '5': 'mayo', '6': 'Junio', '7': 'julio', '8': 'agosto', '9': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'}
    
    months_por_years= [months[month_index] for month_index in months_index_list]
    print(f'meses {months_por_years}')
    
    months_list = [{'label': month.title(), 'value': index_month} for month, index_month in zip(months_por_years, months_index_list)]
    print(months_list)
    
    return months_list, months_index_list[-1]



"""
-Peso inicial
valor
fecha

-Peso actual
valor
fecha

-Peso perdido
valor
fecha_inicial fecha_actual

-Mayor peso
valor
fecha

-Menor peso
valor
fecha
"""