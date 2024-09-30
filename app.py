import dash
import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Define las estadísticas base para cada clase
class_stats = {
    'Bárbaro': {
        'Strength': 20,
        'Vigor': 25,
        'Agility': 13,
        'Dexterity': 12,
        'Will': 18,
        'Knowledge': 5,
        'Resourcefulness': 12,
        'Health': 132.5,
        'Move Speed': 300,
    },
    'Pícaro': {
        'Strength': 15,
        'Vigor': 20,
        'Agility': 25,
        'Dexterity': 18,
        'Will': 12,
        'Knowledge': 8,
        'Resourcefulness': 14,
        'Health': 120,
        'Move Speed': 300,
    },
    # Añade más clases según sea necesario
}

# Añadimos las estadísticas de las armas
weapon_stats = {
    'Zweihander': {
        'Nombre': 'Zweihander',
        'Tipo': 'Espada de dos manos',
        'Manos': 2,
        'Daño Base': 50,
        'Peso': 5,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 990, 'Attack': 179},
            {'Daño %': 1.05, 'Windup': 870, 'Attack': 179},
            {'Daño %': 1.10, 'Windup': 870, 'Attack': 179},
        ],
        'Recover': 500,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.8,  # Parte media
            3: 0.6,  # Mango
        },
    },
    'Espada Larga': {
        'Nombre': 'Espada Larga',
        'Tipo': 'Espada de una mano',
        'Manos': 1,
        'Daño Base': 30,
        'Peso': 3,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 700, 'Attack': 150},
            {'Daño %': 1.05, 'Windup': 600, 'Attack': 150},
            {'Daño %': 1.10, 'Windup': 600, 'Attack': 150},
        ],
        'Recover': 400,
        'Impact Zones': {
            1: 1.0,
            2: 0.9,
            3: 0.7,
        },
    },
    'Escudo': {
        'Nombre': 'Escudo',
        'Tipo': 'Escudo',
        'Manos': 1,
        'Daño Base': 10,
        'Peso': 2,
        'Combo': [
            {'Daño %': 0.5, 'Windup': 800, 'Attack': 200},
        ],
        'Recover': 300,
        'Impact Zones': {
            1: 1.0,
            2: 1.0,
            3: 1.0,
        },
    },
    # Añade más armas según sea necesario
}

class CharacterStats:
    def __init__(self, strength, vigor, agility, dexterity, will, knowledge, resourcefulness,
                 add_stats=None, bonus_stats=None,
                 movement_add=0, movement_bonus=0,
                 peso_arma=0, peso_armadura=0):
        self.strength = strength
        self.vigor = vigor
        self.agility = agility
        self.dexterity = dexterity
        self.will = will
        self.knowledge = knowledge
        self.resourcefulness = resourcefulness
        self.base_move_speed = 300  # Velocidad de movimiento base

        # Encantamientos de "Add" y "Bonus" para estadísticas principales
        self.add_stats = add_stats if add_stats else {}
        self.bonus_stats = bonus_stats if bonus_stats else {}

        # Encantamientos para Velocidad de Movimiento
        self.movement_add = movement_add
        self.movement_bonus = movement_bonus

        # Pesos
        self.peso_arma = peso_arma
        self.peso_armadura = peso_armadura

        self.apply_enchantments()
        self.calculate_stats()
        self.calculate_category_stats()

    def apply_enchantments(self):
        # Aplicar encantamientos de "Add" para estadísticas principales
        self.strength += self.add_stats.get('Fuerza', 0)
        self.vigor += self.add_stats.get('Vigor', 0)
        self.agility += self.add_stats.get('Agilidad', 0)
        self.dexterity += self.add_stats.get('Destreza', 0)
        self.will += self.add_stats.get('Voluntad', 0)
        self.knowledge += self.add_stats.get('Conocimiento', 0)
        self.resourcefulness += self.add_stats.get('Ingenio', 0)

    def calculate_stats(self):
        # Redondear atributos después de aplicar encantamientos
        self.strength = round(self.strength, 2)
        self.vigor = round(self.vigor, 2)
        self.agility = round(self.agility, 2)
        self.dexterity = round(self.dexterity, 2)
        self.will = round(self.will, 2)
        self.knowledge = round(self.knowledge, 2)
        self.resourcefulness = round(self.resourcefulness, 2)

        self.physical_power = self.strength
        self.base_health = self.calculate_base_health()
        self.action_speed = self.calculate_action_speed()
        self.move_speed_modifier = self.calculate_move_speed()

        # Calcular Move Speed Rating total
        # Penalización por peso de armadura se considera como Gear Move Speed negativo
        gear_move_speed = -self.calculate_armor_penalty()
        total_movement_add = self.movement_add + gear_move_speed

        # Move Speed Rating antes del Move Speed Bonus (%)
        self.total_move_speed = self.base_move_speed + self.move_speed_modifier + total_movement_add

        # Convertir a % Move Speed
        percent_move_speed = self.total_move_speed / 3

        # Añadir Move Speed Bonus (%)
        percent_move_speed += self.movement_bonus

        # Reconversión a Move Speed Rating
        self.total_move_speed = percent_move_speed * 3

        # Cap de Move Speed a 330 (110%)
        self.total_move_speed = min(self.total_move_speed, 330)

        # Asegurarnos de que la velocidad no sea negativa
        self.total_move_speed = max(0, round(self.total_move_speed, 2))

    def calculate_base_health(self):
        sum_stats = self.strength * 0.25 + self.vigor * 0.75
        if sum_stats <= 10:
            return 75 + 3 * sum_stats
        elif 10 < sum_stats <= 50:
            return 105 + 2 * (sum_stats - 10)
        elif 50 < sum_stats <= 75:
            return 185 + 1 * (sum_stats - 50)
        elif 75 < sum_stats <= 100:
            return 210 + 0.5 * (sum_stats - 75)
        else:
            return 222.5

    def calculate_action_speed(self):
        sum_stats = self.agility * 0.25 + self.dexterity * 0.75
        if sum_stats <= 10:
            return -38 + 3 * sum_stats
        elif 10 < sum_stats <= 13:
            return -8 + 2 * (sum_stats - 10)
        elif 13 < sum_stats <= 25:
            return -2 + 1 * (sum_stats - 13)
        elif 25 < sum_stats <= 41:
            return 10 + 1.5 * (sum_stats - 25)
        elif 41 < sum_stats <= 50:
            return 34 + 1 * (sum_stats - 41)
        elif 50 < sum_stats <= 100:
            return 43 + 0.5 * (sum_stats - 50)
        else:
            return 68

    def calculate_move_speed(self):
        if self.agility <= 0:
            return -10
        elif 0 < self.agility <= 10:
            return -10 + 0.5 * self.agility
        elif 10 < self.agility <= 15:
            return -5 + 1 * (self.agility - 10)
        elif 15 < self.agility <= 75:
            return 0 + 0.75 * (self.agility - 15)
        elif 75 < self.agility <= 100:
            return 45 + 0.5 * (self.agility - 75)
        else:
            return 57.5

    def calculate_armor_penalty(self):
        return self.peso_armadura * 1.0

    def calculate_category_stats(self):
        penalizacion_arma = self.peso_arma * 1.0
        velocidad_con_arma = self.total_move_speed - penalizacion_arma
        velocidad_con_arma = max(0, round(velocidad_con_arma, 2))  # No puede ser negativa

        # Movement
        self.movement_stats = {
            'Velocidad de Movimiento': f'{self.total_move_speed:.2f}',
            'Peso de arma': f'{self.peso_arma}',
            'Peso de armadura': f'{self.peso_armadura}',
            'Velocidad de movimiento con arma': f'{velocidad_con_arma:.2f}',
        }

        # Damage
        self.damage_stats = {
            'Bono de Poder Físico': f'{self.calculate_physical_power_bonus():.2f}%',
            'Poder Físico': f'{self.physical_power:.2f}',
            'Velocidad de Acción': f'{self.action_speed:.2f}%',
        }

        # Defense
        self.defense_stats = {
            'Salud Base': f'{self.base_health:.2f}'
        }

        # Utility
        self.utility_stats = {
            'Ingenio': f'{self.resourcefulness:.2f}'
        }

    def calculate_physical_power_bonus(self):
        if self.physical_power <= 5:
            bonus = -80 + 10 * self.physical_power
        elif 5 < self.physical_power <= 7:
            bonus = -30 + 5 * (self.physical_power - 5)
        elif 7 < self.physical_power <= 11:
            bonus = -20 + 3 * (self.physical_power - 7)
        elif 11 < self.physical_power <= 15:
            bonus = -8 + 2 * (self.physical_power - 11)
        elif 15 < self.physical_power <= 50:
            bonus = 0 + 1 * (self.physical_power - 15)
        elif 50 < self.physical_power <= 100:
            bonus = 35 + 0.5 * (self.physical_power - 50)
        else:
            return 60  # Máximo según la tabla
        return bonus

    def calculate_attack_damage(self, base_damage, attack_multiplier, impact_zone_multiplier, headshot=False):
        # Cálculo básico del daño
        damage = base_damage * attack_multiplier * impact_zone_multiplier
        # Aplicar bono de Poder Físico
        physical_power_bonus = self.calculate_physical_power_bonus() / 100
        damage *= (1 + physical_power_bonus)
        # Aplicar modificador de headshot si corresponde
        if headshot:
            damage *= 1.5  # Supongamos que el headshot multiplica el daño por 1.5
        return damage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
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

# Callback para actualizar las opciones de armas y deshabilitar inputs
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

if __name__ == '__main__':
    app.run_server(debug=True)
