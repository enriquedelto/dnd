# models/character.py

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
