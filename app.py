# %%
from dash import Dash, html, dcc, callback, Input, Output, dash_table

app = Dash(__name__, external_stylesheets=['assets/style.css'])
server = app.server

app.layout = (
    html.Div(
        className='recuadro-inicio-de-sesion',
        children=[
            html.H1('Welcome', style={})
        ]
    )
)

if __name__ == '__main__':
    app.run_server(port=8050)
# %%
