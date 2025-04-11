from dash import register_page, html, dcc, callback, Input, Output
from conectar_db import *
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pgo

register_page(__name__, path='/dashboard')

pesos_id = ['peso_inicial', 'peso_actual', 'peso_perdido', 'peso_mayor', 'peso_menor', 'peso_prom', 'peso_perd_prom']
pesos_id_totales = [peso_id+'_total' for peso_id in pesos_id]
pesos_id_relativos = [peso_id+'_relativo' for peso_id in pesos_id]

layout = html.Main(children=[
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    html.Link(rel='stylesheet', href='assets/dashboard.css'),
    # -------------------------------------------------------------------------------------------------------------------------------
    html.Div(className= 'div_contenedor_opciones_principales', children=[
        dcc.Dropdown( id = 'dropdown_years', clearable=False, searchable=False, multi=False, style={'width': '100px'},),
        dcc.Dropdown( id = 'dropdown_months', clearable=False, searchable=False, multi=False, style={'width': '200px',},),
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
    # Graficos
    html.Div(id='div_contenedor_graficos', children=[
        html.Div(id='grafico_total'),
        html.Div(id='grafico_relativo'),
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
    # Peso actual total
    query = query=crear_query('fecha', 'MAX')
    valor = consulta_db(query, obtener_datos='uno')
    valores['peso_actual_total'] = valor[0]
    fechas['peso_actual_total'] = valor[1]
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso perdido total
    valores['peso_perdido_total'] = valores['peso_actual_total'] - valores['peso_inicial_total']
    # Obtener los dias que han pasado desde el peso inicial hasta el peso actual
    fecha_1 = datetime.strptime(str(fechas['peso_inicial_total']), "%Y-%m-%d")
    fecha_2 = datetime.strptime(str(fechas['peso_actual_total']), "%Y-%m-%d")
    dias_peso_perdido = (fecha_2 - fecha_1).days
    fechas['peso_perdido_total'] = str(dias_peso_perdido) + ' Días'
    
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
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso promedio Total
    query = f'SELECT AVG(diurno) FROM progreso_peso_{usuario}'
    valor = consulta_db(query, obtener_datos='uno')
    valores['peso_prom_total'] = round(valor[0], 2)
    fechas['peso_prom_total'] = ''
    
    #-----------------------------------------------------------------------------------------------------------------
    # Peso perdido en promedio total
    if dias_peso_perdido == 0:
        valor = '0'
        pass
    else:
        valor = round(valores['peso_perdido_total'] / dias_peso_perdido, 3)
    valores['peso_perd_prom_total'] = valor
    fechas['peso_perd_prom_total'] = 'Por día'
    
    #-----------------------------------------------------------------------------------------------------------------
    resultado = [
        html.Div(children=[
            html.P(str(valores[valor])+ ' Kg', className='p_peso_valor'),
            html.P(fechas[fecha], className='p_peso_fecha'),
        ])
        for valor, fecha in zip(valores, fechas)
    ]
    return resultado

@callback(
    [
        Output(component_id=peso_id_relativo, component_property='children')
        for peso_id_relativo in pesos_id_relativos
    ],
    Input(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='dropdown_years', component_property='value'),
    Input(component_id='dropdown_months', component_property='value'),
)
def actualizar_pesos_relativos(data, year_seleccionado, month_seleccionado):
    usuario = data['sesion_iniciada_por']
    tabla = f'progreso_peso_{usuario}'
    
    #
    valores_peso = {peso_id_relativo: 'null' for peso_id_relativo in pesos_id_relativos}
    fechas_peso = {peso_id_relativo: 'null' for peso_id_relativo in pesos_id_relativos}
    def obtener_datos(columna_nombre, tipo):
        query = f"""
        SELECT diurno, fecha FROM {tabla}
        WHERE EXTRACT(YEAR FROM fecha) = {year_seleccionado}
        AND EXTRACT(MONTH FROM fecha) = {month_seleccionado}
        ORDER BY {columna_nombre} {tipo}
        LIMIT 1
        """
        resultado = consulta_db(query=query, obtener_datos='uno')
        return resultado
    #-----------------------------------------------------------------------------------------------------------------
    # peso inicial relativo
    valor = obtener_datos('fecha', 'ASC')
    valores_peso['peso_inicial_relativo'] = valor[0]
    fechas_peso['peso_inicial_relativo'] = valor[1]
    #-----------------------------------------------------------------------------------------------------------------
    # Peso actual relativo
    valor = obtener_datos('diurno', 'ASC')
    valores_peso['peso_actual_relativo'] = valor[0]
    fechas_peso['peso_actual_relativo'] = valor[1]
    
    # Peso perdido relativo
    valores_peso['peso_perdido_relativo'] = valores_peso['peso_actual_relativo'] - valores_peso['peso_inicial_relativo']
    formato = '%Y-%m-%d'
    fecha_1 = datetime.strptime(str(fechas_peso['peso_inicial_relativo']), formato)
    fecha_2 = datetime.strptime(str(fechas_peso['peso_actual_relativo']), formato)
    dias_peso_perdido = (fecha_2 - fecha_1).days
    fechas_peso['peso_perdido_relativo'] = str(dias_peso_perdido) + ' Días'
    
    # Peso Mayor relativo 
    valor = obtener_datos('diurno', 'DESC')
    valores_peso['peso_mayor_relativo'] = valor[0]
    fechas_peso['peso_mayor_relativo'] = valor[1]
    
    # Peso Menor relativo
    valor = obtener_datos('diurno', 'ASC')
    valores_peso['peso_menor_relativo'] = valor[0]
    fechas_peso['peso_menor_relativo'] = valor[1]
    
    # Peso promedio relativo
    query = f"""
    SELECT AVG(diurno) FROM {tabla}
    WHERE EXTRACT(YEAR FROM fecha) = {year_seleccionado}
    AND EXTRACT(MONTH FROM fecha) = {month_seleccionado}
    """
    valor = round(consulta_db(query, 'uno')[0], 2)
    valores_peso['peso_prom_relativo'] = valor
    fechas_peso['peso_prom_relativo'] = ''
    
    # Peso promedio perdido relativo
    # Evita divisiones por 0
    if dias_peso_perdido == 0:
        valores_peso['peso_perd_prom_relativo'] = 0
    else:
        valor = round(valores_peso['peso_perdido_relativo'] / dias_peso_perdido, 3)
        valores_peso['peso_perd_prom_relativo'] = valor
    fechas_peso['peso_perd_prom_relativo'] = 'Por día'
    
    #-----------------------------------------------------------------------------------------------------------------
    resultado = [
        html.Div(children=[
            html.P(str(valores_peso[valor_peso]) + ' Kg', className='p_peso_valor'),
            html.P(fechas_peso[fecha_peso], className='p_peso_fecha'),
        ])
        for valor_peso, fecha_peso in zip(valores_peso, fechas_peso)
    ]
    return resultado

# Graficos
@callback(
    Output(component_id='grafico_total', component_property='children'),
    Input(component_id='almacenamiento_datos', component_property='data'),
)
def actualizar_grafico_total(data):
    usuario = data['sesion_iniciada_por']
    
    #crear conexion con la base de datos
    conn = conectar_db()
    
    # crear consulta
    query = f"SELECT diurno, fecha FROM progreso_peso_{usuario} ORDER BY fecha"
    
    # obtener datos de la base de datos
    data_base = pd.read_sql(query, conn)
    
    data_base['fecha'] = pd.to_datetime(data_base['fecha'])
    
    # cerrar conexion
    conn.close()
    
    # crear grafico
    fig = px.line(
        data_base,
        x='fecha',
        y='diurno',
        title='Evolucion del peso Total',
        labels={"diurno": 'Peso (Kg)', 'fecha': 'Fecha'},
        markers=True,
        template='plotly_white',
    )
    fig.update_traces(line=dict(color='black'))
    
    peso_promedio = data_base['diurno'].mean()
    fig.add_trace(
        pgo.Scatter(
            x=data_base['fecha'],
            y = [peso_promedio] * len(data_base),
            mode='lines',
            line={'color': 'gray', 'dash': 'dash'},
            name='Promedio',
        )
    )
    
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='center',
            x=0.5,
        ),
        title=dict(x=0.5,)
    )
    
    return dcc.Graph(
        figure = fig,
        config={
            'scrollZoom': False,
            'displaylogo': False,
            'modeBarButtonsToRemove': [
                'select2d',     # desactiva selección rectangular
                'lasso2d',      # desactiva selección lazo
                'autoScale2d',  # desactiva "auto escala"
            ],
        },
        className='grafico',
    )

@callback(
    Output(component_id='grafico_relativo', component_property='children'),
    Input(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='dropdown_years', component_property='value'),
)
def actualizar_grafico_relativo(data, year_seleccionado):
    usuario = data['sesion_iniciada_por']
    tabla = f'progreso_peso_{usuario}'
    
    # crear consulta
    query =f'''
    SELECT diurno, fecha FROM {tabla}
    WHERE EXTRACT(YEAR FROM fecha) = {year_seleccionado}
    ORDER BY fecha
    '''
    
    # conectar a base de datos
    conn = conectar_db()
    
    # crear data frame
    data_base = pd.read_sql(query, conn)
    
    # convertir a formato fecha
    data_base['fecha'] = pd.to_datetime(data_base['fecha'])
    
    # crear nueva columna del mes
    data_base['mes'] = data_base['fecha'].dt.month
    data_base['dia'] = data_base['fecha'].dt.day
    
    fig = px.line(
        data_base,
        x='dia',
        y='diurno',
        color= 'mes',
        template='plotly_white',
        markers=True,
        title= 'Comparacion del peso diario entre meses',
        labels={
            'diurno': 'Peso (Kg)',
            'dia': 'Día del mes',
            'mes': 'Mes',
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Calcular el promedio del peso diurno
    promedio_peso = data_base['diurno'].mean()
    
    fig.add_trace(
        pgo.Scatter(
            x=data_base['dia'],
            y=[promedio_peso] * len(data_base),
            mode='lines',
            line=dict(color='gray', dash='dash'),
            name='Promedio'
        )
    )
    fig.update_layout(title={'x': 0.5})
    return dcc.Graph(
        figure = fig,
        config={'displaylogo': False,},
        className='grafico'
    )