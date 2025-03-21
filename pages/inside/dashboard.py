from dash import register_page, html, dcc, callback, Input, Output
from conectar_db import *

register_page(__name__, path='/dashboard')

pesos_id = ['peso_inicial', 'peso_actual', 'peso_perdido', 'mayor_peso', 'menor_peso']
meses = {'1': 'enero', '2': 'febrero', '3': 'marzo', '4': 'abril', '5': 'mayo', '6': 'Junio', '7': 'julio', '8': 'agosto', '9': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'}

layout = html.Main(children=[
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    html.Link(rel='stylesheet', href='assets/dashboard.css'),
    # ------------------------------------------------------------------
    html.Div(className= 'div_contenedor_opciones_principales', children=[
        html.P('Año: '),
        dcc.Dropdown(
            id = 'dropdown_years',
            clearable=False,
            searchable=False,
            style={'width': '200px'}
            ),
        html.P('Mes: '),
        dcc.Dropdown(
            id = 'dropdown_months',
            clearable=False,
            searchable=False,
            style={'width': '200px'}
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
    print(years_db, bool(not years_db))
    if not years_db:
        resultado = [{'label': 'No hay registros', 'value': 'null'}]
        value = 'null'
        return resultado, value  
    
    years_list = [str(year[0]) for year in years_db]
    years_list.append('Todos')
    print(f'year_list {years_list}')
    
    resultado = [
        {'label': year, 'value': (year).lower()}
        for year in years_list
    ]
    
    # Obtener el valor que se va a mostrar al cargar la pagina en el dropdown years
    value = str(years_list[-2])
    
    return resultado, value

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