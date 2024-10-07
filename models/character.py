from data import weapon_stats


class CharacterStats:
    def __init__(self, strength, vigor, agility, dexterity, will, knowledge, resourcefulness,
                 add_stats=None, bonus_stats=None,
                 movement_add=0, movement_bonus=0,
                 weapon_weight=0, armor_weight=0):
        self.strength = strength
        self.vigor = vigor
        self.agility = agility
        self.dexterity = dexterity
        self.will = will
        self.knowledge = knowledge
        self.resourcefulness = resourcefulness
        self.base_move_speed = 300

        self.add_stats = add_stats if add_stats else {}
        self.bonus_stats = bonus_stats if bonus_stats else {}

        self.movement_add = movement_add
        self.movement_bonus = movement_bonus

        self.weapon_weight = weapon_weight
        self.armor_weight = armor_weight

        # Enchantment stats
        self.physical_power_add = 0
        self.physical_power_bonus = 0
        self.magical_power_add = 0
        self.magical_power_bonus = 0
        self.armor_rating_add = 0
        self.armor_rating_bonus = 0
        self.impact_power_add = 0
        self.impact_power_bonus = 0
        self.health_add = 0
        self.health_bonus = 0
        self.action_speed_add = 0
        self.action_speed_bonus = 0

        # Max Spell Count
        self.base_max_spell_count = 5  # Valor base para Wizard
        self.max_spell_count_bonus = 1  # Multiplicador, inicializado en 1 (sin bonus)

        self.apply_enchantments()
        self.calculate_stats()
        self.calculate_category_stats()

    def apply_enchantments(self):
        self.strength += self.add_stats.get('Strength', 0)
        self.vigor += self.add_stats.get('Vigor', 0)
        self.agility += self.add_stats.get('Agility', 0)
        self.dexterity += self.add_stats.get('Dexterity', 0)
        self.will += self.add_stats.get('Will', 0)
        self.knowledge += self.add_stats.get('Knowledge', 0)
        self.resourcefulness += self.add_stats.get('Resourcefulness', 0)

    def calculate_stats(self):
        self.strength = round(self.strength, 2)
        self.vigor = round(self.vigor, 2)
        self.agility = round(self.agility, 2)
        self.dexterity = round(self.dexterity, 2)
        self.will = round(self.will, 2)
        self.knowledge = round(self.knowledge, 2)
        self.resourcefulness = round(self.resourcefulness, 2)

        self.physical_power = self.strength
        self.magical_power = self.will
        self.armor_rating = self.calculate_armor_rating()
        self.impact_power = self.calculate_impact_power()
        self.item_swap_speed = self.calculate_item_swap_speed()
        self.wearing_time_speed = self.calculate_wearing_time_speed()

        self.base_health = self.calculate_base_health()
        self.action_speed = self.calculate_action_speed()
        self.regular_interaction_speed = self.calculate_regular_interaction_speed()

        self.move_speed_modifier = self.calculate_move_speed()

        gear_move_speed = -self.calculate_armor_penalty()
        total_movement_add = self.movement_add + gear_move_speed

        self.total_move_speed = self.base_move_speed + self.move_speed_modifier + total_movement_add

        percent_move_speed = self.total_move_speed / 3

        percent_move_speed += self.movement_bonus

        self.total_move_speed = percent_move_speed * 3

        self.total_move_speed = min(self.total_move_speed, 330)

        self.total_move_speed = max(0, round(self.total_move_speed, 2))

        self.action_speed_rating = self.calculate_action_speed_rating()
        self.action_speed_percent = self.calculate_action_speed_percent()

        self.calculate_max_spell_count()

    def calculate_max_spell_count(self):
        self.max_spell_count = int(self.base_max_spell_count * self.max_spell_count_bonus)

    def calculate_armor_rating(self):
        return 100 * (1 + self.get_item_armor_rating_bonus())

    def get_item_armor_rating_bonus(self):
        return 0

    def calculate_impact_power(self):
        return 10

    def calculate_item_swap_speed(self):
        return self.action_speed

    def calculate_wearing_time_speed(self):
        return self.calculate_item_equip_speed()

    def calculate_item_equip_speed(self):
        if self.dexterity <= 0:
            return -0.95
        elif self.dexterity <= 1:
            return -0.95
        elif self.dexterity <= 2:
            return -0.91
        elif self.dexterity <= 15:
            return -0.91 + 0.07 * (self.dexterity - 2)
        elif self.dexterity <= 35:
            return 0 + 0.05 * (self.dexterity - 15)
        elif self.dexterity <= 70:
            return 1 + 0.02 * (self.dexterity - 35)
        else:
            return 1.7 + 0.01 * (self.dexterity - 70)

    def calculate_base_health(self):
        health_rating = self.strength * 0.25 + self.vigor * 0.75
        if health_rating <= 10:
            return 75 + 3 * health_rating
        elif health_rating <= 50:
            return 105 + 2 * (health_rating - 10)
        elif health_rating <= 75:
            return 185 + (health_rating - 50)
        elif health_rating <= 100:
            return 210 + 0.5 * (health_rating - 75)
        else:
            return 222.5

    def calculate_action_speed(self):
        speed_rating = self.agility * 0.25 + self.dexterity * 0.75
        if speed_rating <= 10:
            return -0.38 + 0.03 * speed_rating
        elif speed_rating <= 13:
            return -0.08 + 0.02 * (speed_rating - 10)
        elif speed_rating <= 25:
            return -0.02 + 0.01 * (speed_rating - 13)
        elif speed_rating <= 41:
            return 0.10 + 0.015 * (speed_rating - 25)
        elif speed_rating <= 50:
            return 0.34 + 0.01 * (speed_rating - 41)
        elif speed_rating <= 100:
            return 0.43 + 0.005 * (speed_rating - 50)
        else:
            return 0.68

    def calculate_regular_interaction_speed(self):
        speed_rating = self.agility * 0.4 + self.resourcefulness * 0.6
        if speed_rating <= 7:
            return -0.26 + 0.02 * speed_rating
        elif speed_rating <= 15:
            return -0.12 + 0.015 * (speed_rating - 7)
        elif speed_rating <= 20:
            return 0 + 0.07 * (speed_rating - 15)
        elif speed_rating <= 25:
            return 0.35 + 0.06 * (speed_rating - 20)
        elif speed_rating <= 30:
            return 0.65 + 0.05 * (speed_rating - 25)
        elif speed_rating <= 35:
            return 0.90 + 0.04 * (speed_rating - 30)
        elif speed_rating <= 40:
            return 1.10 + 0.03 * (speed_rating - 35)
        elif speed_rating <= 45:
            return 1.25 + 0.02 * (speed_rating - 40)
        elif speed_rating <= 100:
            return 1.35 + 0.01 * (speed_rating - 45)
        else:
            return 1.90

    def calculate_action_speed_rating(self):
        return self.agility * 0.25 + self.dexterity * 0.75

    def calculate_action_speed_percent(self):
        rating = self.action_speed_rating
        percent = -38

        if rating <= 0:
            percent = -38
        elif 0 < rating <= 10:
            percent = -38 + 3 * rating
        elif 10 < rating <= 13:
            percent = -8 + 2 * (rating - 10)
        elif 13 < rating <= 25:
            percent = -2 + 1 * (rating - 13)
        elif 25 < rating <= 41:
            percent = 10 + 1.5 * (rating - 25)
        elif 41 < rating <= 50:
            percent = 34 + 1 * (rating - 41)
        elif 50 < rating <= 100:
            percent = 43 + 0.5 * (rating - 50)
        else:
            percent = 68

        return min(percent, 68)

    def calculate_action_speed_factor(self):
        return 1 / (1 + self.action_speed_percent / 100)

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
        return self.armor_weight * 1.0

    def calculate_category_stats(self):
        weapon_penalty = self.weapon_weight * 1.0
        speed_with_weapon = self.total_move_speed - weapon_penalty
        speed_with_weapon = max(0, round(speed_with_weapon, 2))

        self.movement_stats = {
            'Movement Speed': f'{self.total_move_speed:.2f}',
            'Weapon Weight': f'{self.weapon_weight}',
            'Armor Weight': f'{self.armor_weight}',
            'Movement Speed with Weapon': f'{speed_with_weapon:.2f}',
        }

        self.damage_stats = {
            'Physical Power Bonus': f'{self.calculate_physical_power_bonus():.2f}%',
            'Physical Power': f'{self.physical_power:.2f}',
            'Action Speed': f'{self.action_speed_percent:.2f}%',
        }

        self.defense_stats = {
            'Base Health': f'{self.base_health:.2f}'
        }

        self.utility_stats = {
            'Resourcefulness': f'{self.resourcefulness:.2f}',
            'Max Spell Count': f'{self.max_spell_count}'
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
            return 60
        return bonus

    def calculate_attack_damage(self, base_damage, attack_multiplier, impact_zone_multiplier, headshot=False):
        damage = base_damage * attack_multiplier * impact_zone_multiplier
        physical_power_bonus = self.calculate_physical_power_bonus() / 100
        damage *= (1 + physical_power_bonus)
        if headshot:
            damage *= 1.5
        return damage

    def set_weapon_damage(self, weapon_name, current_damage):
        weapon = weapon_stats.get(weapon_name)
        if not weapon:
            raise ValueError("Weapon not found.")
        
        min_damage = weapon.get('Minimum Damage', weapon.get('Base Damage'))
        max_damage = weapon.get('Maximum Damage', weapon.get('Base Damage'))
        
        if not (min_damage <= current_damage <= max_damage):
            raise ValueError(f"Damage must be between {min_damage} and {max_damage} for {weapon_name}.")

        self.current_weapon_damage = current_damage

    def get_all_stats(self):
        self.calculate_category_stats()
        return {
            'Movement Stats': self.movement_stats,
            'Damage Stats': self.damage_stats,
            'Defense Stats': self.defense_stats,
            'Utility Stats': self.utility_stats,
            'Base Stats': {
                'Strength': f'{self.strength:.2f}',
                'Vigor': f'{self.vigor:.2f}',
                'Agility': f'{self.agility:.2f}',
                'Dexterity': f'{self.dexterity:.2f}',
                'Will': f'{self.will:.2f}',
                'Knowledge': f'{self.knowledge:.2f}',
                'Resourcefulness': f'{self.resourcefulness:.2f}',
            }
        }