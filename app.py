from dash import Dash, html, dcc, page_container, callback, Input, Output
import os


app = Dash(
    __name__,
    use_pages=True, # Permite que se puedan registrar otras paginas
    suppress_callback_exceptions=True, # Esto evitará que Dash arroje errores cuando el callback se defina antes de que el componente aparezca en el layout.
)

server = app.server

app.layout = html.Div([
    html.Link(rel='stylesheet', href='assets/menu_de_paginas.css',),
    dcc.Store('almacenamiento_datos', storage_type='session'), # almacena y obtiene los datos de sesion
    dcc.Location(id='path', refresh=True), # Obtiene la path de la pagina actual
    #---------------------------------------------------------------------------------------------------------
    html.Div(id = 'menu_de_paginas_contenedor', style={'display': 'none'}),
    page_container,
])


# mostrar encabezado de las paginas despues de iniciar sesion
@callback(
    Output(component_id='menu_de_paginas_contenedor', component_property='children'),
    Output(component_id='menu_de_paginas_contenedor', component_property='style'),
    Output(component_id='path', component_property='pathname'), # Este output es para rederigir / a /login si no se ha iniciado sesion
    Input(component_id='almacenamiento_datos', component_property='data'),
    Input(component_id='path', component_property='pathname'),
)

def lista_paginas(
    data, path, 
    ):
    print(f'path actual: {path}')
    print(f'datos de sesion: {data}')
    
    # Si se esta dentro de la pagina principal o no se ha iniciado sesion, no mostrar menu d paginas
    if path=='/' or path=='/login' or not data:
        return '' , {'display': 'none'}, '/login'
    
    # Obtener la lista de las paginas dentro de la carpeta pages/inside
    carpeta = 'pages/inside'
    lista_paginas = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.py')]
    
    # Quitar extension .py de los arhivos
    lista_paginas = [os.path.splitext(archivo)[0] for archivo in lista_paginas]
    print(f'lista de paginas obtenidas: {lista_paginas}')
    
    # Crear los links de las paginas
    lista_paginas = [dcc.Link(archivo, href=archivo, className='pagina_de_menu') for archivo in lista_paginas]
    
    print('-'*100)
    return lista_paginas, {'display': 'flex'}, path


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
