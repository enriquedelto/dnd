# components/layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table
from data import class_stats, weapon_stats

def create_layout(app):
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Calculadora de Estadísticas', className='text-center mb-4'), width=12)
        ]),

        dbc.Row([
            # Sección de Parámetros (izquierda)
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Parámetros', className='card-title'),
                        # Selector de Clase
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Clase', html_for='input-clase'),
                                dcc.Dropdown(
                                    id='input-clase',
                                    options=[{'label': clase, 'value': clase} for clase in class_stats.keys()],
                                    value='Bárbaro'
                                ),
                            ])
                        ], className='mb-3'),

                        # Tablas de Estadísticas
                        dash_table.DataTable(
                            id='stats-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística', 'type': 'text'},
                                {'name': 'Valor', 'id': 'Valor', 'type': 'numeric', 'editable': False},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowY': 'auto'},
                        ),
                        html.Hr(),
                        html.H5('Movimiento', className='mt-3'),
                        dash_table.DataTable(
                            id='movement-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística', 'type': 'text'},
                                {'name': 'Valor', 'id': 'Valor', 'type': 'numeric', 'editable': False},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                                {'name': 'Bonus', 'id': 'Bonus', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowY': 'auto'},
                        ),
                        html.Hr(),
                        html.H5('Defensa', className='mt-3'),
                        dash_table.DataTable(
                            id='defense-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística', 'type': 'text'},
                                {'name': 'Valor', 'id': 'Valor', 'type': 'numeric', 'editable': False},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowY': 'auto'},
                        ),
                        html.Hr(),
                        html.H5('Utilidad', className='mt-3'),
                        dash_table.DataTable(
                            id='utility-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística', 'type': 'text'},
                                {'name': 'Valor', 'id': 'Valor', 'type': 'numeric', 'editable': False},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowY': 'auto'},
                        ),
                    ]),
                ], className='mb-4'),
            ], width=4),

            # Sección de Resultados (derecha)
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Resultados', className='card-title'),
                        # Menú desplegable para seleccionar tipo de resultado
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Seleccionar Tipo de Resultado', html_for='result_type_select'),
                                dcc.Dropdown(
                                    id='result_type_select',
                                    options=[
                                        {'label': 'Daño', 'value': 'damage'},
                                        {'label': 'Velocidad de Movimiento', 'value': 'movement_speed'},
                                    ],
                                    value='damage',
                                ),
                            ], width=6),
                        ], className='mb-3'),

                        # Contenedor para mostrar los resultados
                        html.Div(id='results_output'),
                    ]),
                ]),
            ], width=8),
        ]),

    ], fluid=True)

    return layout