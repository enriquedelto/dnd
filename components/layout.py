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
                        # Selección de Armas
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Arma Izquierda', html_for='weapon1_left'),
                                dcc.Dropdown(
                                    id='weapon1_left',
                                    options=[{'label': w['Nombre'], 'value': w['Nombre']} for w in weapon_stats.values()],
                                    value=None,
                                    disabled=False
                                ),
                            ]),
                            dbc.Col([
                                dbc.Label('Arma Derecha', html_for='weapon1_right'),
                                dcc.Dropdown(
                                    id='weapon1_right',
                                    options=[{'label': w['Nombre'], 'value': w['Nombre']} for w in weapon_stats.values()],
                                    value=None,
                                    disabled=False
                                ),
                            ]),
                        ], className='mb-3'),
                        # Selección de Segunda Arma (Opcional)
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Segunda Arma Izquierda', html_for='weapon2_left'),
                                dcc.Dropdown(
                                    id='weapon2_left',
                                    options=[{'label': w['Nombre'], 'value': w['Nombre']} for w in weapon_stats.values()],
                                    value=None,
                                    disabled=False
                                ),
                            ]),
                            dbc.Col([
                                dbc.Label('Segunda Arma Derecha', html_for='weapon2_right'),
                                dcc.Dropdown(
                                    id='weapon2_right',
                                    options=[{'label': w['Nombre'], 'value': w['Nombre']} for w in weapon_stats.values()],
                                    value=None,
                                    disabled=False
                                ),
                            ]),
                        ], className='mb-3'),
                        # Selección de Tipo de Combate
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Tipo de Combate', html_for='combat_type'),
                                dcc.Dropdown(
                                    id='combat_type',
                                    options=[
                                        {'label': 'Arma', 'value': 'weapon'},
                                        {'label': 'Magia', 'value': 'magic'},
                                        {'label': 'Mixto', 'value': 'mixed'},
                                    ],
                                    value='weapon'
                                ),
                            ])
                        ], className='mb-3'),
                        # Selección de Combinación
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Combinación de Ataques', html_for='combination_select'),
                                dcc.Dropdown(
                                    id='combination_select',
                                    options=[
                                        {'label': 'Combinación 1', 'value': 'comb1'},
                                        {'label': 'Combinación 2', 'value': 'comb2'},
                                        {'label': 'Combinación 3', 'value': 'comb3'},
                                    ],
                                    value='comb1'
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
                        # Agregar menú desplegable para seleccionar tipo de resultado
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