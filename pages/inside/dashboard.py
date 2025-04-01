from dash import register_page, html, dcc, callback, Input, Output
from conectar_db import *
from datetime import datetime

register_page(__name__, path='/dashboard')

pesos_id = ['peso_inicial', 'peso_final', 'peso_perdido', 'peso_mayor', 'peso_menor', 'peso_perdido_prom']
pesos_id_totales = [peso_id+'_total' for peso_id in pesos_id]
pesos_id_relativos = [peso_id+'_relativo' for peso_id in pesos_id]

layout = html.Main(children=[
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    html.Link(rel='stylesheet', href='assets/dashboard.css'),
    # -------------------------------------------------------------------------------------------------------------------------------
    html.Div(className= 'div_contenedor_opciones_principales', children=[
        dcc.Dropdown( id = 'dropdown_years', clearable=False, searchable=False, multi=False, style={'width': '300px'},),
        dcc.Dropdown( id = 'dropdown_months', clearable=False, searchable=False, multi=False, style={'width': '500px',},),
    ]),
    # Pesos totales
    html.Div(className='div_contenedor_pesos', children=[
        *[html.Div(className= 'div_peso', children=[
            html.P(peso_id_total.replace("_", " ").title(), className='p_peso_texto'),
            html.Div(id=peso_id_total)
        ])
        for peso_id_total in pesos_id_totales]
    ]),
    # Pesos relativos
    html.Div(className='div_contenedor_pesos', children=[
        *[html.Div(className='div_peso', children=[
            html.P(peso_relativo.replace('_', ' ').title(), className='p_peso_texto',),
            html.Div(id=peso_relativo)
        ])
        for peso_relativo in pesos_id_relativos] 
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
    
    resultado = [
        {'label': year, 'value': year}
        for year in years_list
    ]
    
    # Obtener el valor que se va a mostrar en el dropdown years
    value = years_list[-1]
    
    return resultado, value

@callback(
    Output(component_id='dropdown_months', component_property='options'),
    Output(component_id='dropdown_months', component_property='value'),
    Input(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='dropdown_years', component_property='value'), # el year es el indice donde se van a obntener los meses
)
def actualizar_dropdown_months(data, year_seleccionado):
    usuario = data['sesion_iniciada_por']
    
    # Obtener la lista de los meses en base al year seleccionado
    query = f"""
    SELECT DISTINCT EXTRACT(MONTH FROM fecha) AS mes
    FROM progreso_peso_{usuario}
    WHERE EXTRACT(YEAR FROM fecha) = {year_seleccionado}
    """
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
        '12': 'diciembre',
    }
    months_options = [{'label': months[month_index].title(), 'value': month_index} for month_index in months_index_list]
    
    return months_options, months_index_list[-1]


@callback(
    [
        Output(component_id=peso_id_total, component_property='children')
        for peso_id_total in pesos_id_totales
    ],
    Input(component_id='almacenamiento_datos', component_property='data')
)
def actualizas_pesos_totales(data):
    usuario = data['sesion_iniciada_por']
    
    valores = {peso_total: 'Sin valor' for peso_total in pesos_id_totales} 
    fechas = {peso_total: 'Sin valor' for peso_total in pesos_id_totales} 
    
    def crear_query(indice, tipo):
        query = f"""
        SELECT diurno, fecha FROM progreso_peso_{usuario}
        WHERE {indice} = (SELECT {tipo}({indice}) FROM progreso_peso_{usuario})
        LIMIT 1
        """
        return query
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso inicial total
    query = query=crear_query('fecha', 'MIN')
    valor = consulta_db(query, obtener_datos='uno')
    valores['peso_inicial_total'] = valor[0]
    fechas['peso_inicial_total'] = valor[1]
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso final total
    query = query=crear_query('fecha', 'MAX')
    valor = consulta_db(query, obtener_datos='uno')
    valores['peso_final_total'] = valor[0]
    fechas['peso_final_total'] = valor[1]
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso perdido total
    valores['peso_perdido_total'] = valores['peso_inicial_total'] - valores['peso_final_total']
    # Obtener los dias que han pasado desde el peso inicial hasta el peso final
    fecha_1 = datetime.strptime(str(fechas['peso_inicial_total']), "%Y-%m-%d")
    fecha_2 = datetime.strptime(str(fechas['peso_final_total']), "%Y-%m-%d")
    dias = (fecha_2 - fecha_1).days
    fechas['peso_perdido_total'] = str(dias) + ' Dias'
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso Maximo Total
    query = crear_query('diurno', 'MAX')
    valor = consulta_db(query, obtener_datos='uno')
    valores['peso_mayor_total'] = valor[0]
    fechas['peso_mayor_total'] = valor[1]
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso Menor Total
    query = crear_query('diurno', 'MIN')
    valor = consulta_db(query, obtener_datos='uno')
    valores['peso_menor_total'] = valor[0]
    fechas['peso_menor_total'] = valor[1]
    
    
    resultado = [
        html.Div(children=[
            html.P(str(valores[valor])+ ' KG', className='p_peso_valor'),
            html.P(fechas[fecha], className='p_peso_fecha'),
        ])
        for valor, fecha in zip(valores, fechas)
    ]
    return resultado