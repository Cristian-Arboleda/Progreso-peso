# %%
from dash import Dash, html, dcc, callback, Input, Output, dash_table

app = Dash(__name__, external_stylesheets=['assets/style.css'])
server = app.server

app.layout = (
    html.Div(
        children=[
            html.Div(
                className='recuadro-inicio-de-sesion',
                children=[
                    html.P(
                        'Iniciar sesion',
                        style={'text-align': 'center', 'font-size': '25px',}
                    ),
                    html.Div(
                        children=[
                            html.Label('Nombre: ', htmlFor='nombre', style={}),
                            dcc.Input(id='nombre')
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Contrasena: ', htmlFor='contrasena', style={}),
                            dcc.Input(id='contrasena')
                        ]
                    )
                ]
            )
        ]
    )
)

if __name__ == '__main__':
    app.run_server(port=8050)
# %%
