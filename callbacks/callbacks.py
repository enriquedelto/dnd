# callbacks/callbacks.py

from dash.dependencies import Input, Output, State, ALL
from dash import html, dcc
from models.character import CharacterStats
from data.class_stats import class_stats
from data.weapon_stats import weapon_stats
import dash_bootstrap_components as dbc
import dash_table

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
            Input('input-class', 'value'),
            Input('stats-table', 'data'),
            Input('movement-table', 'data'),
            Input('result_type_select', 'value'),
            Input({'type': 'dynamic-input', 'index': ALL}, 'value'),
        ],
    )
    def update_statistics(
        selected_class, stats_rows, movement_rows,
        result_type_select, dynamic_input_values
    ):
        # Imprimir los valores de entrada para depuración
        print("Valores de entrada:", dynamic_input_values)

        # Mapeo de IDs a valores
        input_ids = [
            {'type': 'dynamic-input', 'index': 'weapon1_left'},
            {'type': 'dynamic-input', 'index': 'weapon1_right'},
            {'type': 'dynamic-input', 'index': 'weapon2_left'},
            {'type': 'dynamic-input', 'index': 'weapon2_right'},
            {'type': 'dynamic-input', 'index': 'combat_type'},
            {'type': 'dynamic-input', 'index': 'combination_select'},
        ]
        
        # Crear un diccionario de valores, manejando posibles discrepancias en el orden
        dynamic_inputs = {}
        for i, item in enumerate(input_ids):
            if i < len(dynamic_input_values):
                dynamic_inputs[item['index']] = dynamic_input_values[i]
            else:
                dynamic_inputs[item['index']] = None

        # Imprimir el diccionario de entradas para depuración
        print("Dynamic inputs:", dynamic_inputs)

        # Obtener valores de las armas seleccionadas
        weapon1_left = dynamic_inputs.get('weapon1_left')
        weapon1_right = dynamic_inputs.get('weapon1_right')
        weapon2_left = dynamic_inputs.get('weapon2_left')
        weapon2_right = dynamic_inputs.get('weapon2_right')
        combination_select = dynamic_inputs.get('combination_select', 'comb1')

        # Imprimir valores de armas para depuración
        print(f"Armas: {weapon1_left}, {weapon1_right}, {weapon2_left}, {weapon2_right}")
        print(f"Combinación seleccionada: {combination_select}")

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

        if weapon_left and weapon_left in weapon_stats:
            weapon = weapon_stats[weapon_left]
            peso_arma += weapon.get('Weight', 0)
            weapons_selected.append(weapon_left)

        if weapon_right and weapon_right in weapon_stats:
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
        atributos_base = class_stats[selected_class]
        
        # Inicializar encantamientos
        add_stats = {}
        
        # Process stats_table
        if not stats_rows:
            stats_rows = [
                {'Stat': 'Strength', 'Value': atributos_base['Strength'], 'Add': 0},
                {'Stat': 'Vigor', 'Value': atributos_base['Vigor'], 'Add': 0},
                {'Stat': 'Agility', 'Value': atributos_base['Agility'], 'Add': 0},
                {'Stat': 'Dexterity', 'Value': atributos_base['Dexterity'], 'Add': 0},
                {'Stat': 'Will', 'Value': atributos_base['Will'], 'Add': 0},
                {'Stat': 'Knowledge', 'Value': atributos_base['Knowledge'], 'Add': 0},
                {'Stat': 'Resourcefulness', 'Value': atributos_base['Resourcefulness'], 'Add': 0},
            ]
        else:
            for row in stats_rows:
                stat_name = row['Stat']
                add_value = float(row['Add']) if row['Add'] else 0
                add_stats[stat_name] = add_value
        
        # Process movement_table
        movement_add = 0
        movement_bonus = 0
        armor_weight = 0

        if not movement_rows:
            movement_rows = [
                {'Stat': 'Movement Speed', 'Value': '', 'Add': 0, 'Bonus': 0},
                {'Stat': 'Movement Speed with Weapon', 'Value': '', 'Add': '', 'Bonus': ''},
                {'Stat': 'Weapon Weight', 'Value': 0, 'Add': '', 'Bonus': ''},
                {'Stat': 'Armor Weight', 'Value': 0, 'Add': '', 'Bonus': ''},
            ]
        else:
            for row in movement_rows:
                stat_name = row['Stat']
                if stat_name == 'Movement Speed':
                    movement_add = float(row['Add']) if row['Add'] else 0
                    movement_bonus = float(row['Bonus']) if row['Bonus'] else 0
                elif stat_name == 'Armor Weight':
                    armor_weight = float(row['Value']) if row['Value'] else 0

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
            peso_armadura=armor_weight
        )

        # Actualizar los valores en la tabla de estadísticas principales
        for row in stats_rows:
            stat_name = row['Stat']
            if stat_name == 'Strength':
                row['Value'] = character.strength
            elif stat_name == 'Vigor':
                row['Value'] = character.vigor
            elif stat_name == 'Agility':
                row['Value'] = character.agility
            elif stat_name == 'Dexterity':
                row['Value'] = character.dexterity
            elif stat_name == 'Will':
                row['Value'] = character.will
            elif stat_name == 'Knowledge':
                row['Value'] = character.knowledge
            elif stat_name == 'Resourcefulness':
                row['Value'] = character.resourcefulness

        # Actualizar los valores en la tabla de movement
        for row in movement_rows:
            stat_name = row['Stat']
            if stat_name == 'Movement Speed':
                row['Value'] = character.movement_stats['Movement Speed']
            elif stat_name == 'Movement Speed with Weapon':
                row['Value'] = character.movement_stats['Movement Speed with Weapon']
            elif stat_name == 'Weapon Weight':
                row['Value'] = peso_arma
            elif stat_name == 'Armor Weight':
                row['Value'] = armor_weight

        # Preparar datos para las tablas de categorías
        movement_data = movement_rows
        defense_data = [{'Stat': k, 'Value': v} for k, v in character.defense_stats.items()]
        utility_data = [{'Stat': k, 'Value': v} for k, v in character.utility_stats.items()]

        # Preparar contenido de resultados basado en 'result_type_select'
        if result_type_select == 'damage':
            # Obtener armas seleccionadas
            selected_weapons = []
            if combination_select == 'comb1':
                selected_weapons = [weapon1_left, weapon1_right]
            elif combination_select == 'comb2':
                selected_weapons = [weapon2_left, weapon2_right]

            # Filtrar armas no seleccionadas
            selected_weapons = [w for w in selected_weapons if w]

            # Calcular daño por cada arma y ajustar tiempos
            combo_details = []
            total_combo_time = 0
            total_damage = 0
            hit_slowdown_info = []  # Nueva lista para almacenar información de Hit Slowdown

            for weapon_name in selected_weapons:
                weapon = weapon_stats.get(weapon_name)
                if not weapon:
                    continue  # Salta si el arma no está definida

                combo = weapon.get('Combo', [])
                hit_slowdown = weapon.get('Hit Slowdown', {})
                
                # Agregar información de Hit Slowdown si está disponible
                if hit_slowdown:
                    hit_slowdown_info.append({
                        'Weapon': weapon_name,
                        'Percentage': hit_slowdown.get('Percentage', 'N/A'),
                        'Duration': hit_slowdown.get('Duration', 'N/A')
                    })

                for attack in combo:
                    damage_percent = attack.get('Damage %', 1.0)
                    windup = attack.get('Windup', 0)  # En ms
                    attack_time = attack.get('Attack', 0)  # En ms

                    # Calcular daño real
                    base_min_damage = weapon.get('Minimum Damage', weapon.get('Damage', 0))
                    base_max_damage = weapon.get('Maximum Damage', weapon.get('Damage', 0))
                    base_damage = (base_min_damage + base_max_damage) / 2
                    actual_damage = character.calculate_attack_damage(
                        base_damage, damage_percent, 1.0  # Asumiendo Impact Zone 1
                    )
                    total_damage += actual_damage

                    # Ajustar tiempos basados en Action Speed
                    action_speed_factor = character.calculate_action_speed_factor()
                    adjusted_windup = windup * action_speed_factor
                    adjusted_attack_time = attack_time * action_speed_factor

                    total_combo_time += adjusted_windup + adjusted_attack_time

                    combo_details.append({
                        'Weapon': weapon_name,
                        'Damage (%)': f"{damage_percent*100:.1f}%",
                        'Actual Damage': f"{actual_damage:.2f}",
                        'Windup (ms)': f"{adjusted_windup:.2f}",
                        'Attack (ms)': f"{adjusted_attack_time:.2f}",
                        'Hit Slowdown (%)': hit_slowdown.get('Percentage', 'N/A'),
                        'Slowdown Duration (s)': hit_slowdown.get('Duration', 'N/A'),
                    })

            # Crear una tabla de detalles del combo
            combo_table = dash_table.DataTable(
                columns=[
                    {'name': 'Weapon', 'id': 'Weapon'},
                    {'name': 'Damage (%)', 'id': 'Damage (%)'},
                    {'name': 'Actual Damage', 'id': 'Actual Damage'},
                    {'name': 'Windup (ms)', 'id': 'Windup (ms)'},
                    {'name': 'Attack (ms)', 'id': 'Attack (ms)'},
                    {'name': 'Hit Slowdown (%)', 'id': 'Hit Slowdown (%)'},
                    {'name': 'Slowdown Duration (s)', 'id': 'Slowdown Duration (s)'},
                ],
                data=combo_details,
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'fontWeight': 'bold'},
                style_table={'overflowX': 'auto'},
            )

            # Crear información de Hit Slowdown
            hit_slowdown_content = []
            if hit_slowdown_info:
                hit_slowdown_content = [
                    html.H5('Hit Slowdown'),
                    html.Ul([
                        html.Li([
                            f"{info['Weapon']}: ",
                            f"Percentage: {info['Percentage']}%, ",
                            f"Duration: {info['Duration']} seconds"
                        ]) for info in hit_slowdown_info
                    ])
                ]

            # Mostrar tiempo total del combo y daño total
            summary = html.Div([
                html.H5('Combo Summary'),
                html.P(f"Total Combo Damage: {round(total_damage, 2)}"),
                html.P(f"Total Combo Time: {round(total_combo_time, 2)} ms"),
                combo_table,
                html.Hr(),
            ] + hit_slowdown_content)  # Agregar información de Hit Slowdown al resumen

            results_content = html.Div([
                # ... [componentes existentes para selección de armas y tipos de combate] ...
                html.Hr(),
                html.H5('Damage Results'),
                summary,
            ])
        elif result_type_select == 'movement_speed':
            movement_speed = character.movement_stats.get('Movement Speed', 'N/A')
            movement_speed_with_weapon = character.movement_stats.get('Movement Speed with Weapon', 'N/A')

            results_content = html.Div([
                html.H5('Movement Speed'),
                html.P(f"Total Movement Speed: {movement_speed}"),
                html.P(f"Movement Speed with Weapon: {movement_speed_with_weapon}"),
            ])
        else:
            results_content = html.P('Select a result type.')

        return (
            stats_rows,
            movement_data,
            defense_data,
            utility_data,
            results_content,
        )
