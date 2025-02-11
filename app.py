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
                        style={'text-align': 'center', 'font-size': '25px', 'margin': '0px',d}
                    ),
                    html.Div(
                        children=[
                            dcc.Input(id='nombre', className='input-inicio-sesion', placeholder='Nombre de usuario', type='text')
                        ]
                    ),
                    html.Div(
                        children=[
                            dcc.Input(id='contrasena', className='input-inicio-sesion', placeholder='Password', type='password')
                        ]
                    ),
                    html.Button(
                        'Enviar',
                        id='button-inicio-sesion'
                    )
                ]
            )
        ]
    )
)

if __name__ == '__main__':
    app.run_server(port=8050)
# %%
