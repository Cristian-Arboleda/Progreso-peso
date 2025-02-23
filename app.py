from dash import Dash, html
import os

app = Dash(
    __name__,
    use_pages=True,
)

app.server

app.layout =html.Div([
    
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Render asigna el puerto en PORT
    app.run_server(host="0.0.0.0", port=port, debug=False)