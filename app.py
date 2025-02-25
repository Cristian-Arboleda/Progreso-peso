from dash import Dash, html, dcc, page_container, callback, Input, Output, State
import os


app = Dash(
    __name__,
    use_pages=True, # Permite que se puedan registrar otras paginas
    suppress_callback_exceptions=True, # Esto evitará que Dash arroje errores cuando el callback se defina antes de que el componente aparezca en el layout.
)

server = app.server

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='assets/menu_de_paginas.css'
    ),
    html.Div(id = 'menu_de_paginas_contenedor'),
    page_container,
    dcc.Store('almacenamiento_datos', storage_type='session')
])


# mostrar encabezado de las paginas despues de iniciar sesion
@callback(
    Output(component_id='menu_de_paginas_contenedor', component_property='children'),
    Input(component_id='almacenamiento_datos', component_property='data'),
)

def lista_paginas(data):
    if not data:
        return ''
    
    # Obtener la lista de las paginas dentro de la carpeta pages e inside
    carpeta = 'pages/inside'
    lista_paginas = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.py')]
    
    # Quitar extension .py de los arhivos
    
    lista_paginas = [os.path.splitext(archivo)[0] for archivo in lista_paginas]
    
    # Crear los links de las paginas
    
    lista_paginas = [dcc.Link(archivo, href=archivo, className='pagina_de_menu') for archivo in lista_paginas]
    return lista_paginas


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)