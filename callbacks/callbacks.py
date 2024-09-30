# callbacks/callbacks.py

from dash.dependencies import Input, Output, State, ALL
from dash import html, dcc
import plotly.graph_objs as go
from models import CharacterStats
from data import class_stats, weapon_stats
import dash_bootstrap_components as dbc

def register_callbacks(app):

    @app.callback(
        [
            Output('weapon1_left', 'options'),
            Output('weapon1_right', 'options'),
            Output('weapon2_left', 'options'),
            Output('weapon2_right', 'options'),
            Output('weapon1_left', 'disabled'),
            Output('weapon1_right', 'disabled'),
            Output('weapon2_left', 'disabled'),
            Output('weapon2_right', 'disabled'),
            Output('stats-table', 'data'),
            Output('movement-table', 'data'),
            Output('defense-table', 'data'),
            Output('utility-table', 'data'),
            Output('grafica-vm', 'figure'),
            Output('output-vm-total', 'children'),
            Output('output-porcentaje-vm', 'children'),
            Output('output-mejora-optima', 'children'),
            Output('primary_combo', 'children'),
        ],
        [
            Input('input-clase', 'value'),
            Input('stats-table', 'data'),
            Input('movement-table', 'data'),
            Input('weapon1_left', 'value'),
            Input('weapon1_right', 'value'),
            Input('weapon2_left', 'value'),
            Input('weapon2_right', 'value'),
            Input('combat_type', 'value'),
            Input('show_headshot', 'value'),
            Input('combination_select', 'value'),
        ],
    )
    def actualizar_estadisticas(
        clase_seleccionada, stats_rows, movement_rows,
        weapon1_left, weapon1_right, weapon2_left, weapon2_right,
        combat_type, show_headshot, combination_select,
    ):
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
        peso_arma = 0
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

        # Calcular el peso de las armas seleccionadas
        weapons_selected = [weapon1_left, weapon1_right, weapon2_left, weapon2_right]
        for weapon_name in weapons_selected:
            if weapon_name:
                weapon = weapon_stats[weapon_name]
                peso_arma += weapon.get('Peso', 0)

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

        # Opciones iniciales de armas
        all_weapon_options = [
            {'label': weapon['Nombre'], 'value': weapon_name}
            for weapon_name, weapon in weapon_stats.items()
        ]

        # Función auxiliar para filtrar opciones
        def filtrar_opciones(seleccion_opuesta):
            if seleccion_opuesta:
                weapon_opuesta = weapon_stats[seleccion_opuesta]
                if weapon_opuesta['Manos'] == 2:
                    return []
                else:
                    return [
                        {'label': weapon['Nombre'], 'value': weapon_name}
                        for weapon_name, weapon in weapon_stats.items()
                        if weapon['Manos'] == 1
                    ]
            else:
                return all_weapon_options

        # Combinación 1
        weapon1_left_options = filtrar_opciones(weapon1_right)
        weapon1_right_options = filtrar_opciones(weapon1_left)
        weapon1_left_disabled = False
        weapon1_right_disabled = False

        if weapon1_right:
            weapon = weapon_stats[weapon1_right]
            if weapon['Manos'] == 2:
                weapon1_left_disabled = True
        if weapon1_left:
            weapon = weapon_stats[weapon1_left]
            if weapon['Manos'] == 2:
                weapon1_right_disabled = True

        # Combinación 2
        weapon2_left_options = filtrar_opciones(weapon2_right)
        weapon2_right_options = filtrar_opciones(weapon2_left)
        weapon2_left_disabled = False
        weapon2_right_disabled = False

        if weapon2_right:
            weapon = weapon_stats[weapon2_right]
            if weapon['Manos'] == 2:
                weapon2_left_disabled = True
        if weapon2_left:
            weapon = weapon_stats[weapon2_left]
            if weapon['Manos'] == 2:
                weapon2_right_disabled = True

        # Preparar datos para las tablas de categorías
        movement_data = movement_rows
        defense_data = [{'Estadística': k, 'Valor': v} for k, v in character.defense_stats.items()]
        utility_data = [{'Estadística': k, 'Valor': v} for k, v in character.utility_stats.items()]

        # Gráfica
        figura = go.Figure(data=[
            go.Bar(
                x=['Agilidad', 'Fuerza', 'Vigor'],
                y=[character.agility, character.strength, character.vigor],
                text=[character.agility, character.strength, character.vigor],
                textposition='auto',
            )
        ])
        figura.update_layout(
            title='Atributos del Personaje',
            yaxis_title='Valor',
            xaxis_title='Atributos',
            barmode='stack'
        )

        # Cálculo de VM actual
        vm_total_actual = float(character.movement_stats['Velocidad de Movimiento'])
        porcentaje_vm_actual = vm_total_actual / 3

        # Mejora sugerida
        mejoras = {}
        for stat in ['Fuerza', 'Vigor', 'Agilidad', 'Destreza', 'Voluntad', 'Conocimiento', 'Ingenio']:
            new_add_stats = add_stats.copy()
            new_add_stats[stat] = new_add_stats.get(stat, 0) + 1
            character_mejorado = CharacterStats(
                strength=atributos_base['Strength'],
                vigor=atributos_base['Vigor'],
                agility=atributos_base['Agility'],
                dexterity=atributos_base['Dexterity'],
                will=atributos_base['Will'],
                knowledge=atributos_base['Knowledge'],
                resourcefulness=atributos_base['Resourcefulness'],
                add_stats=new_add_stats,
                movement_add=movement_add,
                movement_bonus=movement_bonus,
                peso_arma=peso_arma,
                peso_armadura=peso_armadura
            )
            nueva_vm = float(character_mejorado.movement_stats['Velocidad de Movimiento'])
            mejoras[stat] = nueva_vm - vm_total_actual

        mejoras_ordenadas = sorted(mejoras.items(), key=lambda x: x[1], reverse=True)

        mejora_texto = 'Mejores mejoras al siguiente punto:\n'
        for idx, (estadistica, valor_mejora) in enumerate(mejoras_ordenadas, 1):
            mejora_texto += f'{idx}. {estadistica} (+{valor_mejora:.2f} VM)\n'

        # Seleccionar el arma según la combinación seleccionada
        if combination_select == 'comb1':
            weapon_left = weapon1_left
            weapon_right = weapon1_right
        else:
            weapon_left = weapon2_left
            weapon_right = weapon2_right

        # Generar la sección de Primary Combo
        primary_combo_elements = []

        # Por simplicidad, consideramos solo el arma de la mano derecha si existe
        if weapon_right:
            selected_weapon = weapon_stats.get(weapon_right)
        elif weapon_left:
            selected_weapon = weapon_stats.get(weapon_left)
        else:
            selected_weapon = None

        if selected_weapon and combat_type == 'weapon':
            # Obtener los detalles del combo
            combo = selected_weapon.get('Combo', [])
            impact_zones = selected_weapon.get('Impact Zones', {})
            base_damage = selected_weapon.get('Daño Base', 0)

            # Crear una lista para almacenar las filas de ataques
            primary_combo_rows = []
            current_row = []

            for idx, attack in enumerate(combo):
                attack_num = idx + 1
                # Crear input para Impact Zone
                impact_zone_input = dcc.Input(
                    id={'type': 'impact_zone', 'index': idx},
                    type='number',
                    min=1, max=3, step=1,
                    value=1,  # Valor por defecto
                    style={'width': '60px', 'display': 'inline-block', 'marginLeft': '10px'}
                )

                # Obtener el valor de la Impact Zone
                impact_zone = 1  # Valor por defecto
                impact_zone_value = impact_zones.get(impact_zone, 1.0)

                # Calcular daño
                attack_multiplier = attack['Daño %']
                damage = character.calculate_attack_damage(
                    base_damage, attack_multiplier, impact_zone_value, headshot=False
                )
                damage_headshot = character.calculate_attack_damage(
                    base_damage, attack_multiplier, impact_zone_value, headshot=True
                )

                # Formatear el daño
                if 'show_headshot' in show_headshot:
                    display_damage = f"{damage_headshot:.2f}"
                else:
                    display_damage = f"{damage:.2f} (HS: {damage_headshot:.2f})"

                # Tiempos
                windup = attack['Windup']
                attack_time = attack['Attack']

                # Construir la información del ataque
                attack_info = html.Div([
                    html.Div([
                        html.Span(f'Ataque {attack_num}', style={'fontWeight': 'bold'}),
                        html.Span(' Impact Zone: ', style={'marginLeft': '10px'}),
                        impact_zone_input,
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    html.Div([
                        html.Span(f"Daño: {display_damage}", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    ], style={'marginTop': '5px'}),
                    html.Div([
                        html.Span(f"Windup: {windup} ms", style={'marginRight': '20px'}),
                        html.Span(f"Attack: {attack_time} ms"),
                    ], style={'marginTop': '5px'}),
                ], style={'border': '1px solid #ccc', 'padding': '10px', 'marginBottom': '10px'})

                # Añadir el ataque a la fila actual
                current_row.append(dbc.Col(attack_info, width=6))

                # Si tenemos dos ataques en la fila o es el último ataque, añadimos la fila a las filas principales
                if len(current_row) == 2 or idx == len(combo) - 1:
                    primary_combo_rows.append(dbc.Row(current_row, style={'marginBottom': '10px'}))
                    current_row = []

            # Asignar las filas al elemento principal
            primary_combo_elements = primary_combo_rows

        else:
            primary_combo_elements.append(html.P('No hay arma seleccionada o el tipo de combate es "Spell Combat".'))

        return (
            weapon1_left_options,
            weapon1_right_options,
            weapon2_left_options,
            weapon2_right_options,
            weapon1_left_disabled,
            weapon1_right_disabled,
            weapon2_left_disabled,
            weapon2_right_disabled,
            stats_rows,
            movement_data,
            defense_data,
            utility_data,
            figura,
            html.Strong(f'Velocidad de Movimiento Total: {vm_total_actual:.2f}'),
            html.Strong(f'Porcentaje de VM: {porcentaje_vm_actual:.2f}%'),
            mejora_texto,
            primary_combo_elements,
        )