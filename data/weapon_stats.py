# data/weapon_stats.py

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
