# callbacks/callbacks.py

from dash.dependencies import Input, Output, State, ALL
from dash import html, dcc
from models.character import CharacterStats
from data.class_stats import class_stats
from data.weapon_stats import weapon_stats
import dash_bootstrap_components as dbc

def obtener_opciones_arma(mano):
    opciones = []
    for weapon_name, weapon in weapon_stats.items():
        uso = weapon.get('Usage', 'both')
        if mano == 'main':
            if uso in ['main', 'both']:
                opciones.append({'label': weapon['Name'], 'value': weapon_name})
        elif mano == 'off':
            if uso in ['off', 'both']:
                opciones.append({'label': weapon['Name'], 'value': weapon_name})
    return opciones

def register_callbacks(app):

    @app.callback(
        [
            Output('stats-table', 'data'),
            Output('movement-table', 'data'),
            Output('defense-table', 'data'),
            Output('utility-table', 'data'),
            Output('results_output', 'children'),
        ],
        [
            Input('input-clase', 'value'),
            Input('stats-table', 'data'),
            Input('movement-table', 'data'),
            Input('result_type_select', 'value'),
            Input({'type': 'dynamic-input', 'index': ALL}, 'value'),  # Nuevo Input dinámico
        ],
    )
    def actualizar_estadisticas(
        clase_seleccionada, stats_rows, movement_rows,
        result_type_select, dynamic_input_values
    ):
        # Mapeo de IDs a valores
        input_ids = [
            {'type': 'dynamic-input', 'index': 'weapon1_left'},
            {'type': 'dynamic-input', 'index': 'weapon1_right'},
            {'type': 'dynamic-input', 'index': 'weapon2_left'},
            {'type': 'dynamic-input', 'index': 'weapon2_right'},
            {'type': 'dynamic-input', 'index': 'combat_type'},
            {'type': 'dynamic-input', 'index': 'combination_select'},
        ]
        # Crear un diccionario de valores
        dynamic_inputs = dict(zip([item['index'] for item in input_ids], dynamic_input_values))

        # Obtener valores de las armas seleccionadas
        weapon1_left = dynamic_inputs.get('weapon1_left')
        weapon1_right = dynamic_inputs.get('weapon1_right')
        weapon2_left = dynamic_inputs.get('weapon2_left')
        weapon2_right = dynamic_inputs.get('weapon2_right')
        combination_select = dynamic_inputs.get('combination_select', 'comb1')

        # Calcular el peso de las armas seleccionadas
        peso_arma = 0
        weapons_selected = []

        # Combinación seleccionada
        if combination_select == 'comb1':
            weapon_left = weapon1_left
            weapon_right = weapon1_right
        else:
            weapon_left = weapon2_left
            weapon_right = weapon2_right

        if weapon_left:
            weapon = weapon_stats[weapon_left]
            peso_arma += weapon.get('Weight', 0)
            weapons_selected.append(weapon_left)

        if weapon_right:
            weapon = weapon_stats[weapon_right]
            peso_arma += weapon.get('Weight', 0)
            weapons_selected.append(weapon_right)

        # Verificar si las armas seleccionadas son de dos manos
        weapon1_right_disabled = False
        weapon2_right_disabled = False

        if weapon1_left:
            weapon = weapon_stats[weapon1_left]
            if weapon['Hand Type'] == 'two-handed':
                weapon1_right_disabled = True

        if weapon2_left:
            weapon = weapon_stats[weapon2_left]
            if weapon['Hand Type'] == 'two-handed':
                weapon2_right_disabled = True

        # Obtener los atributos base de la clase seleccionada
        atributos_base = class_stats[clase_seleccionada]
        
        # Inicializar encantamientos
        add_stats = {}
        
        # Procesar stats_table
        if not stats_rows:
            stats_rows = [
                {'Estadística': 'Fuerza', 'Valor': atributos_base['Strength'], 'Add': 0},
                {'Estadística': 'Vigor', 'Valor': atributos_base['Vigor'], 'Add': 0},
                {'Estadística': 'Agilidad', 'Valor': atributos_base['Agility'], 'Add': 0},
                {'Estadística': 'Destreza', 'Valor': atributos_base['Dexterity'], 'Add': 0},
                {'Estadística': 'Voluntad', 'Valor': atributos_base['Will'], 'Add': 0},
                {'Estadística': 'Conocimiento', 'Valor': atributos_base['Knowledge'], 'Add': 0},
                {'Estadística': 'Ingenio', 'Valor': atributos_base['Resourcefulness'], 'Add': 0},
            ]
        else:
            for row in stats_rows:
                stat_name = row['Estadística']
                add_value = float(row['Add']) if row['Add'] else 0
                add_stats[stat_name] = add_value
        
        # Procesar movement_table
        movement_add = 0
        movement_bonus = 0
        peso_armadura = 0

        if not movement_rows:
            movement_rows = [
                {'Estadística': 'Velocidad de Movimiento', 'Valor': '', 'Add': 0, 'Bonus': 0},
                {'Estadística': 'Velocidad de movimiento con arma', 'Valor': '', 'Add': '', 'Bonus': ''},
                {'Estadística': 'Peso de arma', 'Valor': 0, 'Add': '', 'Bonus': ''},
                {'Estadística': 'Peso de armadura', 'Valor': 0, 'Add': '', 'Bonus': ''},
            ]
        else:
            for row in movement_rows:
                stat_name = row['Estadística']
                if stat_name == 'Velocidad de Movimiento':
                    movement_add = float(row['Add']) if row['Add'] else 0
                    movement_bonus = float(row['Bonus']) if row['Bonus'] else 0
                elif stat_name == 'Peso de armadura':
                    peso_armadura = float(row['Valor']) if row['Valor'] else 0

        # Crear una instancia de CharacterStats
        character = CharacterStats(
            strength=atributos_base['Strength'],
            vigor=atributos_base['Vigor'],
            agility=atributos_base['Agility'],
            dexterity=atributos_base['Dexterity'],
            will=atributos_base['Will'],
            knowledge=atributos_base['Knowledge'],
            resourcefulness=atributos_base['Resourcefulness'],
            add_stats=add_stats,
            movement_add=movement_add,
            movement_bonus=movement_bonus,
            peso_arma=peso_arma,
            peso_armadura=peso_armadura
        )

        # Actualizar los valores en la tabla de estadísticas principales
        for row in stats_rows:
            stat_name = row['Estadística']
            if stat_name == 'Fuerza':
                row['Valor'] = character.strength
            elif stat_name == 'Vigor':
                row['Valor'] = character.vigor
            elif stat_name == 'Agilidad':
                row['Valor'] = character.agility
            elif stat_name == 'Destreza':
                row['Valor'] = character.dexterity
            elif stat_name == 'Voluntad':
                row['Valor'] = character.will
            elif stat_name == 'Conocimiento':
                row['Valor'] = character.knowledge
            elif stat_name == 'Ingenio':
                row['Valor'] = character.resourcefulness

        # Actualizar los valores en la tabla de movement
        for row in movement_rows:
            stat_name = row['Estadística']
            if stat_name == 'Velocidad de Movimiento':
                row['Valor'] = character.movement_stats['Velocidad de Movimiento']
            elif stat_name == 'Velocidad de movimiento con arma':
                row['Valor'] = character.movement_stats['Velocidad de movimiento con arma']
            elif stat_name == 'Peso de arma':
                row['Valor'] = peso_arma
            elif stat_name == 'Peso de armadura':
                row['Valor'] = peso_armadura

        # Preparar datos para las tablas de categorías
        movement_data = movement_rows
        defense_data = [{'Estadística': k, 'Valor': v} for k, v in character.defense_stats.items()]
        utility_data = [{'Estadística': k, 'Valor': v} for k, v in character.utility_stats.items()]

        # Generar contenido de resultados basado en 'result_type_select'
        if result_type_select == 'damage':
            results_content = html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Arma Izquierda', html_for='weapon1_left'),
                        dcc.Dropdown(
                            id={'type': 'dynamic-input', 'index': 'weapon1_left'},
                            options=obtener_opciones_arma('main'),
                            value=weapon1_left,
                        ),
                    ]),
                    dbc.Col([
                        dbc.Label('Arma Derecha', html_for='weapon1_right'),
                        dcc.Dropdown(
                            id={'type': 'dynamic-input', 'index': 'weapon1_right'},
                            options=obtener_opciones_arma('off'),
                            value=weapon1_right,
                            disabled=weapon1_right_disabled
                        ),
                    ]),
                ], className='mb-3'),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Segunda Arma Izquierda', html_for='weapon2_left'),
                        dcc.Dropdown(
                            id={'type': 'dynamic-input', 'index': 'weapon2_left'},
                            options=obtener_opciones_arma('main'),
                            value=weapon2_left,
                        ),
                    ]),
                    dbc.Col([
                        dbc.Label('Segunda Arma Derecha', html_for='weapon2_right'),
                        dcc.Dropdown(
                            id={'type': 'dynamic-input', 'index': 'weapon2_right'},
                            options=obtener_opciones_arma('off'),
                            value=weapon2_right,
                            disabled=weapon2_right_disabled
                        ),
                    ]),
                ], className='mb-3'),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Tipo de Combate', html_for='combat_type'),
                        dcc.Dropdown(
                            id={'type': 'dynamic-input', 'index': 'combat_type'},
                            options=[
                                {'label': 'Arma', 'value': 'weapon'},
                                {'label': 'Magia', 'value': 'magic'},
                                {'label': 'Mixto', 'value': 'mixed'},
                            ],
                            value=dynamic_inputs.get('combat_type', 'weapon')
                        ),
                    ]),
                    dbc.Col([
                        dbc.Label('Combinación de Ataques', html_for='combination_select'),
                        dcc.Dropdown(
                            id={'type': 'dynamic-input', 'index': 'combination_select'},
                            options=[
                                {'label': 'Combinación 1', 'value': 'comb1'},
                                {'label': 'Combinación 2', 'value': 'comb2'},
                                {'label': 'Combinación 3', 'value': 'comb3'},
                            ],
                            value=dynamic_inputs.get('combination_select', 'comb1')
                        ),
                    ]),
                ], className='mb-3'),
                html.Hr(),
                html.H5('Resultados de Daño'),
                # Aquí puedes agregar más detalles sobre el daño calculado
            ])
        elif result_type_select == 'movement_speed':
            movement_speed = character.movement_stats.get('Velocidad de Movimiento', 'N/A')
            movement_speed_with_weapon = character.movement_stats.get('Velocidad de movimiento con arma', 'N/A')

            results_content = html.Div([
                html.H5('Velocidad de Movimiento'),
                html.P(f"Velocidad de Movimiento Total: {movement_speed}"),
                html.P(f"Velocidad de Movimiento con Arma: {movement_speed_with_weapon}"),
            ])
        else:
            results_content = html.P('Selecciona un tipo de resultado.')

        return (
            stats_rows,
            movement_data,
            defense_data,
            utility_data,
            results_content,
        )