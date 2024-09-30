# components/layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table
from data import class_stats

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
                        # Mostrar Estadísticas con Encantamientos
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
                        html.H5('Movement', className='mt-3'),
                        dash_table.DataTable(
                            id='movement-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística', 'type': 'text'},
                                {'name': 'Valor', 'id': 'Valor', 'type': 'any', 'editable': True},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                                {'name': 'Bonus (%)', 'id': 'Bonus', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                        ),
                        html.H5('Damage', className='mt-3'),
                        # Selección de armas
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Arma Mano Izquierda'),
                                dcc.Dropdown(
                                    id='weapon1_left',
                                    options=[],
                                    placeholder='Selecciona un arma',
                                ),
                            ], width=6),
                            dbc.Col([
                                dbc.Label('Arma Mano Derecha'),
                                dcc.Dropdown(
                                    id='weapon1_right',
                                    options=[],
                                    placeholder='Selecciona un arma',
                                ),
                            ], width=6),
                        ], className='mb-3'),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Arma Mano Izquierda 2'),
                                dcc.Dropdown(
                                    id='weapon2_left',
                                    options=[],
                                    placeholder='Selecciona un arma',
                                ),
                            ], width=6),
                            dbc.Col([
                                dbc.Label('Arma Mano Derecha 2'),
                                dcc.Dropdown(
                                    id='weapon2_right',
                                    options=[],
                                    placeholder='Selecciona un arma',
                                ),
                            ], width=6),
                        ], className='mb-3'),
                        # Menú desplegable con opciones "Weapon Combat" y "Spell Combat"
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Tipo de Combate'),
                                dcc.Dropdown(
                                    id='combat_type',
                                    options=[
                                        {'label': 'Weapon Combat', 'value': 'weapon'},
                                        {'label': 'Spell Combat', 'value': 'spell'},
                                    ],
                                    value='weapon',
                                ),
                            ], width=6),
                            # Casilla 'toggle' para mostrar daño con modificador de headshot
                            dbc.Col([
                                dbc.Label('Mostrar daño de Headshot'),
                                dbc.Checklist(
                                    options=[{'label': '', 'value': 'show_headshot'}],
                                    value=[],
                                    id='show_headshot',
                                    switch=True,
                                ),
                            ], width=6, style={'marginTop': '30px'}),
                        ], className='mb-3'),
                        # Menú toggle para seleccionar la combinación
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Seleccionar Combinación'),
                                dcc.RadioItems(
                                    id='combination_select',
                                    options=[
                                        {'label': 'Combinación 1', 'value': 'comb1'},
                                        {'label': 'Combinación 2', 'value': 'comb2'},
                                    ],
                                    value='comb1',
                                    inline=True,
                                ),
                            ]),
                        ], className='mb-3'),
                        # Sección de "Primary Combo"
                        html.H5('Primary Combo', className='mt-3'),
                        html.Div(id='primary_combo'),
                        html.H5('Defense', className='mt-3'),
                        dash_table.DataTable(
                            id='defense-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística'},
                                {'name': 'Valor', 'id': 'Valor'}
                            ],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                        ),
                        html.H5('Utility', className='mt-3'),
                        dash_table.DataTable(
                            id='utility-table',
                            columns=[
                                {'name': 'Estadística', 'id': 'Estadística'},
                                {'name': 'Valor', 'id': 'Valor'}
                            ],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                        ),
                    ]),
                ], className='mb-4'),
            ], width=4),

            # Sección de Resultados (derecha)
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Resultados', className='card-title'),
                        dcc.Graph(id='grafica-vm'),
                        html.Div(id='output-vm-total', className='mt-3'),
                        html.Div(id='output-porcentaje-vm', className='mt-2'),
                        html.H5('Mejoras Sugeridas', className='mt-4'),
                        html.Pre(id='output-mejora-optima', style={'whiteSpace': 'pre-wrap'}),
                    ]),
                ]),
            ], width=8),
        ]),

    ], fluid=True)

    return layout
