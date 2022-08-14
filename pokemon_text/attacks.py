import numpy as np
from .pokemon_types import Typ


class Effekt:
    def __init__(self, name, wahrscheinlichkeit):
        self.name = name
        self.wahrscheinlichkeit = wahrscheinlichkeit


class Effekte:
    paralysieren = Effekt('Paralyse', 10)

    angriff_runter1 = Effekt('Angriff_runter1', 100)
    verteidigung_runter1 = Effekt('Verteidigung_runter1', 100)


class Attacke:
    def __init__(self, name: str, staerke: int, genauigkeit: int, typ: int, ap: int, effekt: Effekt | None = None, critical_level2=False):
        self.name = name
        self.staerke = staerke
        self.genauigkeit = genauigkeit
        self.typ = typ
        self.ap = ap
        self.effekt = effekt
        self.critical_level2 = critical_level2


class AttackenDex:
    Tackle = Attacke('Tackle', 35, 95, Typ.Normal, 35)
    Kratzer = Attacke('Kratzer', 40, 100, Typ.Normal, 35)
    Heuler = Attacke('Heuler', 0, 100, Typ.Normal, 40, Effekte.angriff_runter1)
    Rutenschlag = Attacke('Rutenschlag', 0, 100, Typ.Normal, 30, Effekte.verteidigung_runter1)
    Donnerschock = Attacke('Donnerschock', 40, 100, Typ.Elektro, 30, Effekte.paralysieren)


available_attacks = {
    1: [AttackenDex.Tackle, AttackenDex.Heuler],
    4: [AttackenDex.Kratzer, AttackenDex.Heuler],
    7: [AttackenDex.Tackle, AttackenDex.Rutenschlag],
    25: [AttackenDex.Donnerschock, AttackenDex.Heuler]
}


def attack_hits(attack: Attacke) -> bool:
    return np.random.choice(range(256)) < int(255 * attack.genauigkeit / 100)
