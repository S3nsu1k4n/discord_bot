import math
import numpy as np
from .pokemon_types import POKEMON_TYP, get_attack_effectiveness
from .attacks import Attacke, available_attacks

DEX_NAME = {
    1: 'Bisasam',
    2: 'Bisaknosp',
    3: 'Bisaflor',
    4: 'Glumanda',
    5: 'Glutexo',
    6: 'Glurak',
    7: 'Schiggy',
    8: 'Schillok',
    9: 'Turtok',
    25: 'Pikachu'
}


class AsValues:
    def __init__(self, kp, angriff, verteidigung, spezial, initiative):
        self.kp = kp
        self.angriff = angriff
        self.verteidigung = verteidigung
        self.spezial = spezial
        self.initiative = initiative


AS_WERTE = {
    1: AsValues(45, 49, 49, 65, 45),
    2: AsValues(60, 62, 63, 80, 60),
    3: AsValues(80, 82, 83, 100, 80),
    4: AsValues(39, 52, 43, 50, 65),
    5: AsValues(58, 64, 58, 65, 80),
    6: AsValues(78, 84, 78, 85, 100),
    7: AsValues(44, 48, 65, 50, 43),
    8: AsValues(59, 63, 80, 65, 58),
    9: AsValues(79, 83, 100, 85, 78),
    25: AsValues(35, 55, 40, 50, 90),
}


def get_is_value():
    return np.random.choice(range(16))


class IsValues:
    def __init__(self):
        self.angriff = get_is_value()
        self.verteidigung = get_is_value()
        self.spezial = get_is_value()
        self.initiative = get_is_value()
        self.kp = 8 * (self.angriff % 2) + 4 * (self.verteidigung % 2) + 2 * (self.initiative % 2) + 1 * (self.spezial % 2)


class Stats:
    kp = 0
    kp_momentan = 0
    angriff = 0
    verteidigung = 0
    spezial = 0
    initiative = 0


class Pokemon:
    def __init__(self, dex_id=25, level=5):
        self.dex_id = dex_id
        self.name = DEX_NAME[dex_id]
        self.typ = POKEMON_TYP[dex_id]
        self.level = level
        self.SE = 0  # Statexperience
        self.stats = Stats()
        self.IS = IsValues()
        self.AS = AS_WERTE[self.dex_id]
        self.x = self.update_x()
        self.update_stats()

        self.attacken = available_attacks[dex_id]

    def update_x(self) -> int:
        x = int((math.sqrt(self.SE-1) + 1) / 4) if self.SE != 0 else 0
        return x if x <= 63 else 63

    def update_stats(self):
        y = 5   # 5 bei Statuswerte, bei KP (Level +10)
        self.stats.kp = int(((self.AS.kp + self.IS.kp) * 2 + self.x) * self.level / 100 + (self.level + 10))
        self.stats.kp_momentan = self.stats.kp
        self.stats.angriff = int(((self.AS.angriff + self.IS.angriff) * 2 + self.x) * self.level / 100 + y)
        self.stats.verteidigung = int(((self.AS.verteidigung + self.IS.verteidigung) * 2 + self.x) * self.level / 100 + y)
        self.stats.spezial = int(((self.AS.spezial + self.IS.spezial) * 2 + self.x) * self.level / 100 + y)
        self.stats.initiative = int(((self.AS.initiative + self.IS.initiative) * 2 + self.x) * self.level / 100 + y)

    def get_stats(self):
        return {
            'KP': self.stats.kp,
            'Angriff': self.stats.angriff,
            'Verteidigung': self.stats.verteidigung,
            'Spezial': self.stats.spezial,
            'Initiative': self.stats.initiative,
        }

    def get_kp(self) -> tuple:
        return self.stats.kp_momentan, self.stats.kp

    def receive_damage(self, damage: int):
        self.stats.kp_momentan -= damage
        if self.stats.kp_momentan < 0:
            self.stats.kp_momentan = 0

    def critical_factor(self, stufe_2=False) -> bool:
        thresh = 64 if stufe_2 else 512
        chance = self.AS.initiative / thresh
        chance = chance if chance < 1 else 0.996
        return np.random.choice([2, 1], p=[chance, 1-chance])

    def use_attack(self, attack: Attacke, enemy: 'Pokemon') -> tuple[int, bool]:
        if attack.staerke == 0:
            return 0, False
        critical = self.critical_factor(stufe_2=attack.critical_level2)

        val1 = 2 * self.level * critical / 5 + 2
        angr_vert_ratio = self.stats.angriff / enemy.stats.verteidigung

        damage = val1 * attack.staerke * angr_vert_ratio / 50 + 2

        # calculate stab bonus
        stab = 1.5 if attack.typ in self.typ else 1
        # Calculate Type effectiveness

        type1 = get_attack_effectiveness(attack.typ, enemy.typ[0])
        type2 = get_attack_effectiveness(attack.typ, enemy.typ[1])
        return int(damage * stab * type1 * type2), critical == 2

    def get_fight_display(self, enemy=False) -> str:
        if enemy:
            return f'''
                    {self.name} Lv. {self.level}\n
                    KP: {int(self.stats.kp_momentan / self.stats.kp * 100)}%/100%\n
                    '''
        else:
            return f'''
                {self.name} Lv. {self.level}\n
                KP: {self.stats.kp_momentan}/{self.stats.kp}\n
            '''

    def get_4attack_options(self) -> str:
        return ''.join(str(i) + ': ' + attacke.name + '\n' for i, attacke in enumerate(self.attacken))
