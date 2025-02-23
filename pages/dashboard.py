from dash import register_page, html, dcc, callback, Input, Output

register_page(__name__, path='/dashboard')

layout = html.Div(children=[
    dcc.Store(id='almacenamiento_datos', storage_type='session'),
    html.P(id='mensaje_bienvenida')
])

@callback(
    Output(component_id='mensaje_bienvenida', component_property='children'),
    Input(component_id='almacenamiento_datos', component_property='data'),
)

def update_bienvenida(almacenamiento_datos):
    if not almacenamiento_datos:
        return
    
    print(almacenamiento_datos)
    return f'Bienvenido {almacenamiento_datos['sesion_iniciada_por']}'