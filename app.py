# app.py

from dash import Dash
import dash_bootstrap_components as dbc
from components.layout import create_layout
from callbacks.callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Establecer el layout
app.layout = create_layout(app)

# Registrar los callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
