# callbacks/callbacks.py

from dash.dependencies import Input, Output, State, ALL
from dash import html, dcc
from models.character import CharacterStats
from data.class_stats import class_stats
from data.weapon_stats import weapon_stats
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
            Output('results_output', 'children'),  # Nuevo Output
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
            Input('combination_select', 'value'),
            Input('result_type_select', 'value'),  # Nuevo Input
        ],
    )
    def actualizar_estadisticas(
        clase_seleccionada, stats_rows, movement_rows,
        weapon1_left, weapon1_right, weapon2_left, weapon2_right,
        combat_type, combination_select, result_type_select
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

        # Generar contenido de resultados basado en 'result_type_select'
        if result_type_select == 'damage':
            # Lógica para generar resultados de daño
            # ... (código para calcular y mostrar el daño)
            results_content = html.Div([
                html.H5('Resultados de Daño'),
                # Aquí puedes agregar más detalles sobre el daño calculado
            ])

        elif result_type_select == 'movement_speed':
            # Lógica para generar resultados de velocidad de movimiento
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
            results_content,  # Nuevo retorno
        )