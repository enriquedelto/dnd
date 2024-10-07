# components/layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table
from data import class_stats, weapon_stats
from callbacks.callbacks import obtener_opciones_arma

def create_layout(app):
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Stats Calculator', className='text-center mb-4'), width=12)
        ]),

        dbc.Row([
            # Parameters Section (left)
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Parameters', className='card-title'),
                        # Class Selector
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Class', html_for='input-class'),
                                dcc.Dropdown(
                                    id='input-class',
                                    options=[{'label': class_name, 'value': class_name} for class_name in class_stats.keys()],
                                    value='Barbarian'
                                ),
                            ])
                        ], className='mb-3'),

                        # Stats Tables
                        dash_table.DataTable(
                            id='stats-table',
                            columns=[
                                {'name': 'Stat', 'id': 'Stat', 'type': 'text'},
                                {'name': 'Value', 'id': 'Value', 'type': 'numeric', 'editable': False},
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
                                {'name': 'Stat', 'id': 'Stat', 'type': 'text'},
                                {'name': 'Value', 'id': 'Value', 'type': 'numeric', 'editable': False},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                                {'name': 'Bonus', 'id': 'Bonus', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowY': 'auto'},
                        ),
                        html.Hr(),
                        html.H5('Defense', className='mt-3'),
                        dash_table.DataTable(
                            id='defense-table',
                            columns=[
                                {'name': 'Stat', 'id': 'Stat', 'type': 'text'},
                                {'name': 'Value', 'id': 'Value', 'type': 'numeric', 'editable': False},
                                {'name': 'Add', 'id': 'Add', 'type': 'numeric', 'editable': True},
                            ],
                            data=[],
                            style_cell={'textAlign': 'left', 'padding': '5px'},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowY': 'auto'},
                        ),
                        html.Hr(),
                        html.H5('Utility', className='mt-3'),
                        dash_table.DataTable(
                            id='utility-table',
                            columns=[
                                {'name': 'Stat', 'id': 'Stat', 'type': 'text'},
                                {'name': 'Value', 'id': 'Value', 'type': 'numeric', 'editable': False},
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

            # Results Section (right)
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Results', className='card-title'),
                        
                        # Weapon combination selector
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Weapon Combination', html_for='combination_select'),
                                dcc.Dropdown(
                                    id={'type': 'dynamic-input', 'index': 'combination_select'},
                                    options=[
                                        {'label': 'Combination 1', 'value': 'comb1'},
                                        {'label': 'Combination 2', 'value': 'comb2'},
                                    ],
                                    value='comb1',
                                ),
                            ], width=6),
                        ], className='mb-3'),

                        # Selectors of weapons for Combination 1
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Main Weapon (Combination 1)', html_for='weapon1_left'),
                                dcc.Dropdown(
                                    id={'type': 'dynamic-input', 'index': 'weapon1_left'},
                                    options=obtener_opciones_arma('main'),
                                    value=None,
                                ),
                            ], width=6),
                            dbc.Col([
                                dbc.Label('Offhand Weapon (Combination 1)', html_for='weapon1_right'),
                                dcc.Dropdown(
                                    id={'type': 'dynamic-input', 'index': 'weapon1_right'},
                                    options=obtener_opciones_arma('off'),
                                    value=None,
                                ),
                            ], width=6),
                        ], className='mb-3'),

                        # Selectors of weapons for Combination 2
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Main Weapon (Combination 2)', html_for='weapon2_left'),
                                dcc.Dropdown(
                                    id={'type': 'dynamic-input', 'index': 'weapon2_left'},
                                    options=obtener_opciones_arma('main'),
                                    value=None,
                                ),
                            ], width=6),
                            dbc.Col([
                                dbc.Label('Offhand Weapon (Combination 2)', html_for='weapon2_right'),
                                dcc.Dropdown(
                                    id={'type': 'dynamic-input', 'index': 'weapon2_right'},
                                    options=obtener_opciones_arma('off'),
                                    value=None,
                                ),
                            ], width=6),
                        ], className='mb-3'),

                        # Combat type selector
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Combat Type', html_for='combat_type'),
                                dcc.Dropdown(
                                    id={'type': 'dynamic-input', 'index': 'combat_type'},
                                    options=[
                                        {'label': 'Melee', 'value': 'melee'},
                                        {'label': 'Ranged', 'value': 'ranged'},
                                    ],
                                    value='melee',
                                ),
                            ], width=6),
                        ], className='mb-3'),

                        # Result type selector
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Select Result Type', html_for='result_type_select'),
                                dcc.Dropdown(
                                    id='result_type_select',
                                    options=[
                                        {'label': 'Damage', 'value': 'damage'},
                                        {'label': 'Movement Speed', 'value': 'movement_speed'},
                                    ],
                                    value='damage',
                                ),
                            ], width=6),
                        ], className='mb-3'),

                        # Results output container
                        html.Div(id='results_output'),
                    ]),
                ]),
            ], width=8),
        ]),

    ], fluid=True)

    return layout