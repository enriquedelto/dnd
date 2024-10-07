# data/weapon_stats.py

weapon_stats = {
    'Zweihander': {
        'Name': 'Zweihander',
        'Type': 'Sword',
        'Classes': ['Fighter', 'Barbarian', 'Warlock'],
        'Hand Type': 'two-handed',
        'Usage': 'main',
        'Weight': 40,
        'Minimum Damage': 41,
        'Maximum Damage': 60,
        'Stats': {},
        'Combo': [
            {'Damage %': 1.0, 'Windup': 990, 'Attack': 179},
            {'Damage %': 1.05, 'Windup': 1164, 'Attack': 200},
            {'Damage %': 1.10, 'Windup': 1537, 'Attack': 233},
        ],
        'Action Movement Penalty': {
            'Primary Attacks': {
                'Medium Attack': 0.825,
                'Others': 0.65
            },
            'Secondary Attack 1': {
                'Medium Attack': 0.825,
                'Others': 0.65
            }
        },
        'Hit Slowdown': {
            'Percentage': -0.25,
            'Duration': 1
        },
        'Impact Zones': {
            1: 1.0,
            2: 0.8,
            3: 0.6,
        },
        'Impact Power': 4,
    },
    # Añade más armas según sea necesario
}