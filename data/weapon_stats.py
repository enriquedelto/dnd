# data/weapon_stats.py

weapon_stats = {
    'Bare Hands': {
        'Nombre': 'Bare Hands',
        'Tipo': 'Unarmed',
        'Manos': 0,
        'Daño Mínimo': 10,
        'Daño Máximo': 10,
        'Peso': 0,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 400, 'Attack': 205},
            {'Daño %': 1.0, 'Windup': 450, 'Attack': 200},
        ],
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.9,  # Parte media
            3: 0.8,  # Mango
        },
    },
    'Arming Sword': {
        'Nombre': 'Arming Sword',
        'Tipo': 'Espada de una mano',
        'Manos': 1,
        'Daño Mínimo': 29,
        'Daño Máximo': 41,
        'Peso': 3,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 400, 'Attack': 205},
            {'Daño %': 1.05, 'Windup': 634, 'Attack': 157},
            {'Daño %': 1.10, 'Windup': 976, 'Attack': 154},
        ],
        'Recover': 1213,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.9,  # Parte media
            3: 0.7,  # Mango
        },
    },
    'Crystal Sword': {
        'Nombre': 'Crystal Sword',
        'Tipo': 'Espada de dos manos',
        'Manos': 2,
        'Daño Mínimo': 30,
        'Daño Máximo': 40,
        'Peso': 5,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 550, 'Attack': 168},
            {'Daño %': 1.05, 'Windup': 147, 'Attack': 133},
            {'Daño %': 1.10, 'Windup': 107, 'Attack': 145},
            {'Daño %': 1.15, 'Windup': 330, 'Attack': 167},
        ],
        'Recover': 1068,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.85, # Parte media
            3: 0.65, # Mango
        },
    },
    'Falchion': {
        'Nombre': 'Falchion',
        'Tipo': 'Espada de una mano',
        'Manos': 1,
        'Daño Mínimo': 30,
        'Daño Máximo': 40,
        'Daño Base': 35,
        'Peso': 4,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 680, 'Attack': 133},
            {'Daño %': 1.05, 'Windup': 1174, 'Attack': 127},
            {'Daño %': 1.10, 'Windup': 119, 'Attack': 172},
        ],
        'Recover': 1115,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.9,  # Parte media
            3: 0.75, # Mango
        },
    },
    'Longsword': {
        'Nombre': 'Longsword',
        'Tipo': 'Espada de dos manos',
        'Manos': 2,
        'Daño Mínimo': 34,
        'Daño Máximo': 44,
        'Daño Base': 39,
        'Peso': 6,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 930, 'Attack': 229},
            {'Daño %': 1.05, 'Windup': 906, 'Attack': 233},
            {'Daño %': 1.10, 'Windup': 977, 'Attack': 233},
        ],
        'Recover': 977,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.8,  # Parte media
            3: 0.6,  # Mango
        },
    },
    'Rapier': {
        'Nombre': 'Rapier',
        'Tipo': 'Espada de una mano',
        'Manos': 1,
        'Daño Mínimo': 18,
        'Daño Máximo': 24,
        'Daño Base': 21,
        'Peso': 2,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 450, 'Attack': 56},
            {'Daño %': 1.05, 'Windup': 823, 'Attack': 79},
            {'Daño %': 1.10, 'Windup': 830, 'Attack': 81},
            {'Daño %': 1.15, 'Windup': 880, 'Attack': 83},
        ],
        'Recover': 688,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.88, # Parte media
            3: 0.75, # Mango
        },
    },
    'Short Sword': {
        'Nombre': 'Short Sword',
        'Tipo': 'Espada de una mano',
        'Manos': 1,
        'Daño Mínimo': 19,
        'Daño Máximo': 25,
        'Daño Base': 22,
        'Peso': 2,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 510, 'Attack': 121},
            {'Daño %': 1.05, 'Windup': 600, 'Attack': 133},
            {'Daño %': 1.10, 'Windup': 810, 'Attack': 172},
        ],
        'Recover': 813,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.85, # Parte media
            3: 0.75, # Mango
        },
    },
    'Viking Sword': {
        'Nombre': 'Viking Sword',
        'Tipo': 'Espada de una mano',
        'Manos': 1,
        'Daño Mínimo': 27,
        'Daño Máximo': 35,
        'Daño Base': 31,
        'Peso': 5,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 720, 'Attack': 165},
            {'Daño %': 1.05, 'Windup': 1011, 'Attack': 175},
            {'Daño %': 1.10, 'Windup': 1045, 'Attack': 145},
            {'Daño %': 1.15, 'Windup': 788, 'Attack': 175},
        ],
        'Recover': 788,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.85, # Parte media
            3: 0.7,  # Mango
        },
    },
    'Riposte': {
        'Nombre': 'Riposte',
        'Tipo': 'Ataque Especial',
        'Manos': 1,
        'Daño Mínimo': 22,
        'Daño Máximo': 28,
        'Daño Base': 25,
        'Peso': 4,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 1080, 'Attack': 260},
            {'Daño %': 1.05, 'Windup': 2690, 'Attack': 0},  # Recover sin ataque
        ],
        'Recover': 2690,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.8,  # Parte media
            3: 0.7,  # Mango
        },
    },
    'Zweihander': {
        'Nombre': 'Zweihander',
        'Tipo': 'Espada de dos manos',
        'Manos': 2,
        'Daño Mínimo': 41,
        'Daño Máximo': 60,
        'Daño Base': 50,
        'Peso': 6,
        'Combo': [
            {'Daño %': 1.0, 'Windup': 990, 'Attack': 179},
            {'Daño %': 1.05, 'Windup': 1164, 'Attack': 200},
            {'Daño %': 1.10, 'Windup': 1537, 'Attack': 233},
        ],
        'Recover': 967,
        'Impact Zones': {
            1: 1.0,  # Extremo
            2: 0.8,  # Parte media
            3: 0.6,  # Mango
        },
    },
    # Añade más armas según sea necesario
}